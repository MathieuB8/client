from PyQt5.QtCore import QObject, pyqtSignal
from oauthlib.oauth2 import InsecureTransportError, TokenExpiredError
import json

from decorators import with_logger


# Api request that can get queued until we get authorized.
@with_logger
class ApiRequest(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, manager, request, http_op, opname, auth):
        QObject.__init__(self)
        self._manager = manager
        self._req = request
        self._op = http_op
        self._opname = opname
        self._rep = None
        self._auth = auth
        self._ssl_errors = None

    def run(self):
        if not self._auth or self._manager.is_authorized():
            self.send_request()
        else:
            self._loger.warn('Deferring API Request to wait for auth')
            self._manager.authorized.connect(self.at_auth)

    def send_request(self):
        self._logger.debug('send_request')

        if self._manager.is_authorized():
            self._manager.oauth.add_token(self._req, self._opname)
        self._rep = self._op(self._req)
        self._rep.error.connect(self.on_error)
        self._rep.sslErrors.connect(self.on_ssl_errors)
        self._rep.finished.connect(self.on_finish)

    def at_auth(self):
        self._manager.authorized.disconnect(self.at_auth)
        try:
            self._manager.oauth.add_token(self._req, self._opname)
        except (TokenExpiredError, InsecureTransportError):
            self.error.emit("Oauth expiry / transport error")
            return
        self.send_request()

    def on_error(self, error):
        self._logger.error(error)
        self._rep.error.disconnect()
        self._rep.finished.disconnect()
        self._rep.sslErrors.disconnect()
        del self._manager._requests[self]

        self._error = self._rep.error()

        data = bytes(self._rep.readAll()).decode("utf-8")
        ret = "Reply error {}: {}".format(error, data)
        if self._ssl_errors:
            ret += "\nSSL errors encountered: {}".format(self._ssl_errors)
        self.error.emit(ret)

    def on_ssl_errors(self, errors):
        self._ssl_errors = [str(e.errorString()) for e in errors]

    def on_finish(self):
        self._logger.debug('on_finish')
        try:
            data = bytes(self._rep.readAll()).decode("utf-8")
            resp = json.loads(data)
            self.finished.emit(resp)
        except ValueError:
            self.error.emit("Failed to parse json: " + data)
            self._logger.exception('Failed on_finish')

        del self._manager._requests[self]


class ApiListRequest(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, requests, count):
        QObject.__init__(self)
        self._reqs = requests
        self._nextreq = None
        self._result = []
        self._count = count

    def run(self):
        self._run_next_req()

    def _run_next_req(self):
        try:
            self._nextreq = next(self._reqs)
        except StopIteration:
            self.finished.emit(self._result)
            return
        self._nextreq.finished.connect(self._at_finished)
        self._nextreq.error.connect(self._at_error)
        self._nextreq.run()

    def _at_finished(self, values):
        if not isinstance(values, dict) or "data" not in values:
            self._at_error("Expected a dict response with data")
            return
        items = values["data"]

        if not isinstance(items, list):
            self._at_error("Data is not a list")
            return

        if len(items) == 0:
            self.finished.emit(self._result)
            return

        if len(self._result) + len(items) >= self._count:
            items = items[:self._count - len(self._result)]

        self._result += items
        if len(self._result) >= self._count:
            self.finished.emit(self._result)
            return
        self._run_next_req()

    def _at_error(self, text):
        self._nextreq = None
        self.error.emit(text)
