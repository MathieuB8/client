from oauthlib.oauth2 import LegacyApplicationClient, OAuth2Error, TokenExpiredError
from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QTimer
import base64
import json
from .request import ApiRequest
from config import Settings

from decorators import with_logger


class ApiSettings(object):
    def __init__(self, settings = None):
        if settings is None:
            settings = Settings
        api_p = "api/"
        self.baseUrl = 'https://' + settings.get(api_p + "baseUrl")
        self.clientId = settings.get(api_p + "clientId")
        self.clientSecret = settings.get(api_p + "clientSecret")
        self.accessTokenUri = settings.get(api_p + "accessTokenUri")
        self.refreshToken = settings.get(api_p + "refreshToken")


@with_logger
class OAuthHandler(object):
    """
    Abstracts away grabbing the OAuth authentication token and adding
    tokens to requests. Uses oauthlib.
    We 'gain' token when we receive a reply from the endpoint. We 'lose' it
    when we find out that it expired when trying to add it.
    """
    def __init__(self, settings):
        self._settings = settings
        self._client = LegacyApplicationClient(self._settings.clientId, refresh_token=self._settings.refreshToken)
        self._manager = None
        self._hasToken = False
        self._rep = None

    @property
    def api_manager(self):
        return self._manager

    @api_manager.setter
    def api_manager(self, manager):
        self._manager = manager

    def authorize(self, username, password):
        if password:
            self._logger.info('Trying to log in to api with user/password')
            req = QtNetwork.QNetworkRequest()
            req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
                          'application/x-www-form-urlencoded')
            req.setRawHeader(b'Accept', b'application/json, application/vnd.api+json')
            h_auth = b"Basic " + base64.b64encode(self._settings.clientId.encode() + b":" +
                     self._settings.clientSecret.encode())
            req.setRawHeader(b'Authorization', h_auth)
            self._logger.debug('Preparing token grab with {}:{}'.format(self._settings.clientId,self._settings.clientSecret))

            body = bytes(self._client.prepare_request_body(
                username=username,
                password=password,
                client_id=self._settings.clientId), "utf-8")
            self._rep = self._manager.post(QUrl(self._settings.accessTokenUri),
                                           req, body, auth=False)
            self._rep.finished.connect(self._on_authorized_response)
            self._rep.error.connect(self._on_error)
            self._rep.run()
        elif self._client.refresh_token:
            self._logger.info('Trying to log in to api with refresh token')
            self.refresh()
        else:
            self._on_error('No password or refresh token for api access.')

    def refresh(self):
        req = QtNetwork.QNetworkRequest()
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
                      'application/x-www-form-urlencoded')
        req.setRawHeader(b'Accept', b'application/json, application/vnd.api+json')
        h_auth = b"Basic " + base64.b64encode(self._settings.clientId.encode() + b":" +
                 self._settings.clientSecret.encode())
        req.setRawHeader(b'Authorization', h_auth)

        url, _, body = self._client.prepare_refresh_token_request(self._settings.baseUrl + self._settings.accessTokenUri, client_id=self._settings.clientId)

        self._logger.info(url)
        self._logger.info(body)

        self._rep = self._manager.post(QUrl(url), req, body.encode(), auth=False)
        self._rep.finished.connect(self._on_authorized_response)
        self._rep.error.connect(self._on_error)
        self._rep.run()

    def _on_error(self, text):
        self._rep = None
        self._manager.on_authorize_error(text)

    def _on_authorized_response(self, reply):
        self._rep = None
        try:
            body = json.dumps(reply)    # FIXME
#            self._logger.info(reply)
            self._client.parse_request_body_response(body)
        except OAuth2Error:
            return self._on_error("Failed to parse oauth: " + json.dumps(reply))

        expires_in = reply['expires_in']
        refresh_token = reply['refresh_token']
        Settings.set('api/refreshToken', refresh_token)

        self._hasToken = True
        self._manager.on_authorized(expires_in)

    def add_token(self, request, http_method):
        """
        Adds the token to request headers. If the token expired, does not
        modify request.
        """
        url = str(request.url().toString())
        try:
            _, auth_header, _ = self._client.add_token(
                url,
                token_placement='auth_header',
                http_method=http_method)
        except TokenExpiredError:
            # FIXME - this is an oauth quirk, maybe we're better off checking
            # token expiration on our own?
            self._hasToken = False
            raise

        for hname in auth_header:
            request.setRawHeader(bytes(hname, "utf-8"), bytes(auth_header[hname], "utf-8"))

    def has_token(self):
        return self._hasToken


@with_logger
class ApiManager(QObject):
    """
    Wraps API HTTP communication - queues requests if we're not authorized yet,
    delegates authorization to OAuthHandler, abstracts host.
    """
    authorized = pyqtSignal()
    authorisation_needed = pyqtSignal()

    def __init__(self, network_manager, settings, oauth):
        QObject.__init__(self)
        self._network_manager = network_manager
        self._settings = settings
        self.oauth = oauth
        self.oauth.api_manager = self
        self._ssl_conf = QtNetwork.QSslConfiguration()
        self._ssl_conf.setProtocol(QtNetwork.QSsl.TlsV1_2OrLater)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.oauth.refresh)
        self.timer.setSingleShot(True)
        # Need to keep running requests around so they don't get cleaned up
        # by GC
        self._requests = {}

    def authorize(self, username, password):
        self.oauth.authorize(username, password)

    def on_authorized(self, expires_in):
        self._logger.info('api_manager authorized')

        # expires_in is in seconds
        # timeout is in msecs
        self.timer.start(expires_in * 1000 / 2)

        self.authorized.emit()

    def is_authorized(self):
        return self.oauth.has_token()

    def on_authorize_error(self, text):     # TODO
        print('Error authorizing: ' + text)
        self._logger.error('Error authorizing: %s', text)

    def _op(self, endpoint, request, http_op, op_name, auth=True):
        request.setUrl(QUrl(self._settings.baseUrl).resolved(endpoint))
        request.setSslConfiguration(self._ssl_conf)

        req = ApiRequest(self, request, http_op, op_name, auth)

        self._requests[req] = True

        return req

    def get(self, endpoint, request, auth=False):
        return self._op(endpoint, request, self._network_manager.get, "GET",
                        auth)

    def post(self, endpoint, request, data, auth=True):
        return self._op(endpoint, request,
                        lambda r: self._network_manager.post(r, data), "POST",
                        auth)

    def put(self, endpoint, request, data, auth=True):
        return self._op(endpoint, request,
                        lambda r: self._network_manager.put(r, data), "PUT",
                        auth)

# FIXME - turn everything below into unit tests

from PyQt5.QtWidgets import QApplication
import sys
from .api import Api


class MockSettings(object):
    def __init__(self):
        self.baseUrl = 'https://api.dev.faforever.com'
        self.accessTokenUri = '/oauth/token'
        self.clientId = b'3bc8282c-7730-11e5-8bcf-feff819cdc9f'
        self.clientSecret = b'6035bd78-7730-11e5-8bcf-feff819cdc9f'


LOGIN = "OppressiveDuke"
PASSWORD = "foo"


def do_test(body):
    print("Received!")
    print(body)
    sys.exit(0)


def test_login():
    a = QApplication([])
    settings = MockSettings()
    oauth = OAuthHandler(settings)
    am = QtNetwork.QNetworkAccessManager()
    manager = ApiManager(am, settings, oauth)
    manager.authorize(LOGIN, PASSWORD)
    faf_api = Api(manager)
    req = faf_api._get_all("/data/featuredMod")
    req.finished.connect(do_test)
    req.run()
    a.exec_()

if __name__ == "__main__":
    test_login()
