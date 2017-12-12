
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl
import util
import secondaryServer
import api.methods
import logging
logger = logging.getLogger(__name__)
FormClass, BaseClass = util.THEME.loadUiType("tournaments/tournaments.ui")
from tourneys.tournamentinfo import TournamentInfo


class TournamentsWidget(FormClass, BaseClass):
    """ list and manage the main tournament lister """
    tourneys_general_information_data = ''

    def __init__(self, client, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.client = client
        self.tourneyList.currentItemChanged.connect(self.itemChanged)
        util.THEME.setStyleSheet(self, "tournaments/formatters/style.css")
        self.show_tournaments_informations()

    def itemChanged(self,current,previous):
        text=str(current.data(QtCore.Qt.UserRole).name)+'\n\nDescription : '+str(current.data(QtCore.Qt.UserRole).description)+'\n\nNumber of participants : '+str(current.data(QtCore.Qt.UserRole).number_of_participants)+'\n\nStart time : '+str(current.data(QtCore.Qt.UserRole).start_time)+'\n\nTournament type : '+str(current.data(QtCore.Qt.UserRole).tournament_type)
        self.currentTournamentDetails.setText(str(text))
        url=str(current.data(QtCore.Qt.UserRole).live_image_url)
        self.tournamentsWebView.setUrl(QUrl(url))

    def tourneys_general_information_error(self,resp):
        logger.error('tourneys_general_information error : '+str(resp))
        return -5

    def list_participants_error(self,resp):
        logger.error('list_participants error : '+str(resp))
        return -5

    def tourneys_general_information_result(self,response):
        logger.info('tourneys_general_information_result api response is : ' + str(response))
        self.tourneys_general_information_data = response # hacky way... dunno how to do 2 api calls in a row...
        for alltournaments in reversed(response):
            if alltournaments.get('tournament')!= None and len(alltournaments['tournament']) >= 1:
                myTourney = TournamentInfo()
                myTourney.name = alltournaments['tournament']['name']
                myTourney.state = alltournaments['tournament']['state']
                myTourney.number_of_participants = alltournaments['tournament']['participants_count']
                myTourney.tournament_type = alltournaments['tournament']['tournament_type']
                myTourney.live_image_url = alltournaments['tournament']['live_image_url']
                myTourney.start_time = alltournaments['tournament']['start_at']
                myTourney.full_challonge_url = alltournaments['tournament']['full_challonge_url']
                myTourney.description = alltournaments['tournament']['description']
                myTourney.id = alltournaments['tournament']['id']
                api.methods.list_participants(self.client.Api, myTourney.id, 250, 1, self.list_participants_result(response),  self.list_participants_error)


                item = QtWidgets.QListWidgetItem()
                item.setText(myTourney.name + '\nState : ' + myTourney.state + '\n\n')
                item.setData(QtCore.Qt.UserRole, myTourney)
                self.tourneyList.addItem(item)
        self.tourneyList.show()


    def list_participants_result(self, response, result_first_api_call):
        logger.info('ZAWA 2222 >>>>>>>>>> ' + str(result_first_api_call))
        logger.info('ZAWA 1111111 >>>>>>>> ' + str(result_first_api_call))
        # logger.info('self.tourneys_general_information_data of list_participants_result api response is : '+str(self.tourneys_general_information_data))

        '''for alltournaments in reversed(tourneys_general_information_data):
            if alltournaments.get('tournament')!= None and len(alltournaments['tournament']) >= 1:
                myTourney = TournamentInfo()
                myTourney.name = alltournaments['tournament']['name']
                myTourney.state = alltournaments['tournament']['state']
                myTourney.number_of_participants = alltournaments['tournament']['participants_count']
                myTourney.tournament_type = alltournaments['tournament']['tournament_type']
                myTourney.live_image_url = alltournaments['tournament']['live_image_url']
                myTourney.start_time = alltournaments['tournament']['start_at']
                myTourney.full_challonge_url = alltournaments['tournament']['full_challonge_url']
                myTourney.description = alltournaments['tournament']['description']
                myTourney.id = alltournaments['tournament']['id']
                #result=api.methods.list_participants(self.client.Api, myTourney.id, 250, 1, self.list_participants_result,  self.list_participants_error)
                #logger.info('RESULT PLS ZAWA is : ' + str(result))
                item = QtWidgets.QListWidgetItem()
                item.setText(myTourney.name + '\nState : ' + myTourney.state + '\n\n')
                item.setData(QtCore.Qt.UserRole, myTourney)
                self.tourneyList.addItem(item)'''

        '''for allparticipants in response:
            if (allparticipants['tournament']) >= 1:
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
                item.setText(myTourney.name+'\nState : '+myTourney.state+'\n\n')
                item.setData(QtCore.Qt.UserRole, myTourney)
                self.tourneyList.addItem(item)
        self.tourneyList.show()'''

    def show_tournaments_informations(self):
        result=api.methods.tourneys_general_information(self.client.Api, 250, 1, self.tourneys_general_information_result, self.tourneys_general_information_error)

