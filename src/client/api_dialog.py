from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtWidgets import QCompleter

import util
import logging

logger = logging.getLogger(__name__)

FormClass, BaseClass = util.THEME.loadUiType("client/kick.ui")

class ApiLoginDialog(FormClass, BaseClass):

    def __init__(self, client, *args, **kwargs):
        BaseClass.__init__(self, client, *args, **kwargs)

        self.client = client

        self.setParent(client)

        self.setupUi(self)
        self.setModal(True)
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)

    def accepted(self):
        password = self.lePassword.text()
        self.ApiManager.authorize(self.client.login, password)
        self.hide()

    def rejected(self):
        self.hide()
