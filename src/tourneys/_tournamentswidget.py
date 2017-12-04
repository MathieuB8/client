import webbrowser
from PyQt5.QtCore import Qt
from util.qt import ExternalLinkPage


from PyQt5 import QtCore, QtWidgets
import util
import secondaryServer


FormClass, BaseClass = util.THEME.loadUiType("tournaments/tournaments.ui")

class TournamentsWidget(FormClass, BaseClass):
    """ list and manage the main tournament lister """

    def __init__(self, client, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.client = client

