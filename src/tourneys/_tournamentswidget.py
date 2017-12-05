
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl
import util
import secondaryServer
FormClass, BaseClass = util.THEME.loadUiType("tournaments/tournaments.ui")

from ui.busy_widget import BusyWidget

import api.methods
import logging
logger = logging.getLogger(__name__)

class TournamentInfo():
    def __init(self, client, *args, **kwargs):
        self.name=''
        self.state=''
        self.number_of_participants=''
        self.tournament_type=''
        self.live_image_url=''
        self.start_time=''
        self.full_challonge_url=''
        self.description=''

class TournamentsWidget(FormClass, BaseClass):
    """ list and manage the main tournament lister """

    '''self.textUpQLabel    = QtGui.QLabel()
    self.textDownQLabel  = QtGui.QLabel()

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)'''

    def __init__(self, client, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.client = client


        self.tourneyList.currentItemChanged.connect(self.itemChanged)

        self.tourneysTab = {}
        #item = QListWidgetItem("Item ZAWA")
        self.show_tournaments_informations()
        # Special stylesheet
        util.THEME.setStyleSheet(self, "tournaments/formatters/style.css")

    def itemChanged(self,current,previous):
        #QtWidgets.QMessageBox.about(self.client, "tesZEA", 'BOOM CLICKED')
        text=str(current.data(QtCore.Qt.UserRole).name)+'\nDescription : '+str(current.data(QtCore.Qt.UserRole).description)+'\nNumber of participants : '+str(current.data(QtCore.Qt.UserRole).number_of_participants)+'\nStart time : '+str(current.data(QtCore.Qt.UserRole).start_time)+'\nTournament type : '+str(current.data(QtCore.Qt.UserRole).tournament_type)

        self.currentTournamentDetails.setText(str(text))

        url=str(current.data(QtCore.Qt.UserRole).live_image_url)
        self.tournamentsWebView.setUrl(QUrl(url))

    def tourneys_general_information_error(self,resp):
        logger.error('tourneys_general_information error : '+str(resp))
        return -5


    def tourneys_general_information_result(self,response):
        result=[]
        # Create QCustomQWidget
        logger.info('tourneys_general_information_result api response is : '+str(response))
        for alltournaments in reversed(response):
            if alltournaments.get('tournament')!= None and len(alltournaments['tournament']) >= 1:
                if 1==1 or alltournaments['tournament']['state']=='complete':
                    '''myQCustomQWidget = QCustomQWidget()
                    myQCustomQWidget.setTextUp('zawa')
                    myQCustomQWidget.setTextDown(alltournaments['tournament']['name']+'\nState:'+alltournaments['tournament']['state']+'\n')
                    self.tourneyList.addItem(myQCustomQWidget)'''
                    myTourney = TournamentInfo()
                    myTourney.name = alltournaments['tournament']['name']
                    myTourney.state = alltournaments['tournament']['state']
                    myTourney.number_of_participants = alltournaments['tournament']['participants_count']
                    myTourney.tournament_type = alltournaments['tournament']['tournament_type']
                    myTourney.live_image_url = alltournaments['tournament']['live_image_url']
                    myTourney.start_time = alltournaments['tournament']['start_at']
                    myTourney.full_challonge_url = alltournaments['tournament']['full_challonge_url']
                    myTourney.description = alltournaments['tournament']['description']

                    item = QtWidgets.QListWidgetItem()
                    item.setText(alltournaments['tournament']['name']+'\nState : '+alltournaments['tournament']['state']+'\n\n')
                    item.setData(QtCore.Qt.UserRole, myTourney)
                    self.tourneyList.addItem(item)




                    #item = QtWidgets.QListWidgetItem('A Text-Only Item')
                    #self.tourneyList.addItem(alltournaments['tournament']['name']+'\nState : '+alltournaments['tournament']['state']+'\n\n')

        self.tourneyList.show()

    def show_tournaments_informations(self):
        result=api.methods.tourneys_general_information(self.client.Api,250,1,self.tourneys_general_information_result,self.tourneys_general_information_error)

