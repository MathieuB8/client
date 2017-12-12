from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from fa.replay import replay
import util
import os
import fa
from PyQt5.QtGui import QIcon, QPixmap
from tutorials.tutorialsytvideo import TutorialsVideo
from tutorials.maptutorial import MapTutorial
from achievement.achievements import Achievements
from PyQt5.QtWidgets import QMessageBox


import logging
logger = logging.getLogger(__name__)
FormClass, BaseClass = util.THEME.loadUiType("tutorials/tutorials.ui")


class TutorialsWidget(FormClass, BaseClass):

    video_list = []
    maps_tutorial_list = [[], [], [], []]
    maps_challenge_list = [[], [], [], []]
    current_categorie = 0
    current_challenge_categorie = 0
    current_index_of_video_list = 0
    current_index_of_maps_tutorials_list = [1, 1, 1, 1]
    current_index_of_maps_challenge_list = [1, 1, 1, 1]

    def setup_initial_videos(self):
        initialvideo = TutorialsVideo(
            'https://www.youtube.com/embed/Qhrz0rZmnLU', 'The best tips to improve on forged alliance.')
        self.video_list.append(initialvideo)
        video2 = TutorialsVideo(
            'https://www.youtube.com/embed/tqCs0WVGT_I', 'Guide on how to use the client.')
        self.video_list.append(video2)

        self.show_video(self.current_index_of_video_list)

    def setup_initial_maps_tutorial(self):
        self.map1_pushbutton_tutorials.setFlat(True)
        self.map2_pushbutton_tutorials.setFlat(True)
        self.map3_pushbutton_tutorials.setFlat(True)

        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_Theta_BO')
        self.maps_tutorial_list[0].append(map)
        map = MapTutorial('res/tutorials/map2.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[0].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[0].append(map)
        map = MapTutorial('res/tutorials/map2.png', 'FAF_TUT_Theta_BO')
        self.maps_tutorial_list[0].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_Theta_BO')
        self.maps_tutorial_list[0].append(map)

        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_tutorial_list[1].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_tutorial_list[1].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_tutorial_list[1].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_tutorial_list[1].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_tutorial_list[1].append(map)

        map = MapTutorial('res/tutorials/map5.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[2].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[2].append(map)
        map = MapTutorial('res/tutorials/map5.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[2].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[2].append(map)
        map = MapTutorial('res/tutorials/map5.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[2].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_Loki_BO')
        self.maps_tutorial_list[2].append(map)

        map = MapTutorial('res/tutorials/map6.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_tutorial_list[3].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_tutorial_list[3].append(map)
        map = MapTutorial('res/tutorials/map6.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_tutorial_list[3].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_tutorial_list[3].append(map)
        map = MapTutorial('res/tutorials/map6.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_tutorial_list[3].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_tutorial_list[3].append(map)

        self.set_stylesheet_for_maps(1)

    def setup_initial_challenge_map(self):
        self.map1_challenge_pushbutton_tutorials.setFlat(True)
        self.map2_challenge_pushbutton_tutorials.setFlat(True)
        self.map3_challenge_pushbutton_tutorials.setFlat(True)

        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_Theta_BO')
        self.maps_challenge_list[0].append(map)
        map = MapTutorial('res/tutorials/map2.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[0].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[0].append(map)
        map = MapTutorial('res/tutorials/map2.png', 'FAF_TUT_Theta_BO')
        self.maps_challenge_list[0].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_Theta_BO')
        self.maps_challenge_list[0].append(map)

        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_challenge_list[1].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_challenge_list[1].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_challenge_list[1].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_challenge_list[1].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_SummerDuel_BO')
        self.maps_challenge_list[1].append(map)

        map = MapTutorial('res/tutorials/map5.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[2].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[2].append(map)
        map = MapTutorial('res/tutorials/map5.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[2].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[2].append(map)
        map = MapTutorial('res/tutorials/map5.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[2].append(map)
        map = MapTutorial('res/tutorials/map3.png', 'FAF_TUT_Loki_BO')
        self.maps_challenge_list[2].append(map)

        map = MapTutorial('res/tutorials/map6.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_challenge_list[3].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_challenge_list[3].append(map)
        map = MapTutorial('res/tutorials/map6.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_challenge_list[3].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_challenge_list[3].append(map)
        map = MapTutorial('res/tutorials/map6.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_challenge_list[3].append(map)
        map = MapTutorial('res/tutorials/map1.png', 'FAF_TUT_FourLeaf_BO')
        self.maps_challenge_list[3].append(map)

        self.set_stylesheet_for_challenge(1)

    def set_stylesheet_for_maps(self, index):
        if 1 <= self.current_index_of_maps_tutorials_list[self.current_categorie] <= len(self.maps_tutorial_list[self.current_categorie]) - 2:
            logger.info('previous map zawa22>>' +
                        str(self.current_index_of_maps_tutorials_list[self.current_categorie]))
            self.map1_pushbutton_tutorials.setStyleSheet(
                'border-image: url(' + str(self.maps_tutorial_list[self.current_categorie][index - 1].link) + ');')
            self.map2_pushbutton_tutorials.setStyleSheet(
                'border-image: url(' + str(self.maps_tutorial_list[self.current_categorie][index].link) + ');')
            self.map3_pushbutton_tutorials.setStyleSheet(
                'border-image: url(' + str(self.maps_tutorial_list[self.current_categorie][index + 1].link) + ');')

    def set_stylesheet_for_challenge(self, index):
        if 1 <= self.current_index_of_maps_challenge_list[self.current_challenge_categorie] <= len(self.maps_challenge_list[self.current_challenge_categorie]) - 2:
            logger.info('previous map zawa22>>' +
                        str(self.current_index_of_maps_challenge_list[self.current_challenge_categorie]))
            self.map1_challenge_pushbutton_tutorials.setStyleSheet(
                'border-image: url(' + str(self.maps_challenge_list[self.current_challenge_categorie][index - 1].link) + ');')
            self.map2_challenge_pushbutton_tutorials.setStyleSheet(
                'border-image: url(' + str(self.maps_challenge_list[self.current_challenge_categorie][index].link) + ');')
            self.map3_challenge_pushbutton_tutorials.setStyleSheet(
                'border-image: url(' + str(self.maps_challenge_list[self.current_challenge_categorie][index + 1].link) + ');')

    def update_interactive_images(self):
        logger.info('update called >>>>' +
                    str(self.current_index_of_maps_tutorials_list[self.current_categorie]))
        if 1 <= self.current_index_of_maps_tutorials_list[self.current_categorie] <= len(self.maps_tutorial_list[self.current_categorie]) - 2:
            logger.info('previous map zawa>>>>' +
                        str(self.current_index_of_maps_tutorials_list[self.current_categorie]))
            self.set_stylesheet_for_maps(
                self.current_index_of_maps_tutorials_list[self.current_categorie])

    def update_challenge_images(self):
        if 1 <= self.current_index_of_maps_challenge_list[self.current_challenge_categorie] <= len(self.maps_challenge_list[self.current_challenge_categorie]) - 2:
            logger.info('previous map zawa>>>>' +
                        str(self.current_index_of_maps_challenge_list[self.current_challenge_categorie]))
            self.set_stylesheet_for_challenge(
                self.current_index_of_maps_challenge_list[self.current_challenge_categorie])


    def previous_map(self):
        if self.current_index_of_maps_tutorials_list[self.current_categorie] > 1:
            self.current_index_of_maps_tutorials_list[self.current_categorie] -= 1
            self.update_interactive_images()

    def previous_challenge(self):
        if self.current_index_of_maps_challenge_list[self.current_challenge_categorie] > 1:
            self.current_index_of_maps_challenge_list[self.current_challenge_categorie] -= 1
            self.update_challenge_images()

    def next_map(self):
        logger.info('NEXT MAP CLICKED with the index ' +
                    str(self.current_index_of_maps_tutorials_list[self.current_categorie]))
        if self.current_index_of_maps_tutorials_list[self.current_categorie] < len(self.maps_tutorial_list[self.current_categorie]) - 2:
            logger.info('GG NEXT MAP CLICKED with the index ' +
                        str(self.current_index_of_maps_tutorials_list[self.current_categorie]))
            self.current_index_of_maps_tutorials_list[self.current_categorie] += 1
            self.update_interactive_images()

    def next_challenge(self):
        if self.current_index_of_maps_challenge_list[self.current_challenge_categorie] < len(self.maps_challenge_list[self.current_challenge_categorie]) - 2:
            self.current_index_of_maps_challenge_list[self.current_challenge_categorie] += 1
            self.update_challenge_images()

    def show_video(self, index_of_video):
        if 0 <= index_of_video < len(self.video_list):
            self.video_webengine_tutorials.setUrl(
                self.video_list[index_of_video].link)
            self.description_video_textBrowser_tutorials.setHtml('''<center>
            ''' + self.video_list[index_of_video].description + '''
            </center>''')

    def update_current_interactive_categorie(self, categorie_number):
        self.current_categorie = categorie_number
        self.update_interactive_images()

    def update_current_challenge_categorie(self, categorie_number):
        self.current_challenge_categorie = categorie_number
        self.update_challenge_images()

    def __init__(self, client, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.client = client
        util.THEME.setStyleSheet(self, "tutorials/formatters/style.css")
        self.setup_initial_videos()
        self.setup_initial_maps_tutorial()
        self.setup_initial_challenge_map()

        self.nextvideo_pushbutton_tutorials.clicked.connect(self.next_video)
        self.previousvideo_pushbutton_tutorials.clicked.connect(
            self.previous_video)


        self.previousmap_pushbutton_tutorials.clicked.connect(
            self.previous_map)
        self.nextmap_pushbutton_tutorials.clicked.connect(self.next_map)
        self.map1_pushbutton_tutorials.clicked.connect(
            lambda: self.start_tutorial(-1))
        self.map2_pushbutton_tutorials.clicked.connect(
            lambda: self.start_tutorial(0))
        self.map3_pushbutton_tutorials.clicked.connect(
            lambda: self.start_tutorial(1))

        self.categorie0_pushbutton_interactive_tutorials.toggled.connect(
            lambda: self.update_current_interactive_categorie(0))
        self.categorie1_pushbutton_interactive_tutorials.toggled.connect(
            lambda: self.update_current_interactive_categorie(1))
        self.categorie2_pushbutton_interactive_tutorials.toggled.connect(
            lambda: self.update_current_interactive_categorie(2))
        self.categorie3_pushbutton_interactive_tutorials.toggled.connect(
            lambda: self.update_current_interactive_categorie(3))

            #zawa
        self.previousmap_challenge_pushbutton_tutorials.clicked.connect(
            self.previous_challenge)
        self.nextmap_challenge_pushbutton_tutorials.clicked.connect(self.next_challenge)
        self.map1_challenge_pushbutton_tutorials.clicked.connect(
            lambda: self.start_challenge(-1))
        self.map2_challenge_pushbutton_tutorials.clicked.connect(
            lambda: self.start_challenge(0))
        self.map3_challenge_pushbutton_tutorials.clicked.connect(
            lambda: self.start_challenge(1))

        self.categorie0_pushbutton_challenge_tutorials.toggled.connect(
            lambda: self.update_current_challenge_categorie(0))
        self.categorie1_pushbutton_challenge_tutorials.toggled.connect(
            lambda: self.update_current_challenge_categorie(1))
        self.categorie2_pushbutton_challenge_tutorials.toggled.connect(
            lambda: self.update_current_challenge_categorie(2))
        self.categorie3_pushbutton_challenge_tutorials.toggled.connect(
            lambda: self.update_current_challenge_categorie(3))
            #fin zawa

        self.call_personal_trainer_pushbutton_tutorials.clicked.connect(self.calling_for_personal_trainer)

        self.knowledge_base_texbrowser_tutorials.setHtml('''<center>
        You can find basic information about the game on the wiki :
        <a href='https://wiki.faforever.com/index.php?title=Main_Page'><span style="color:#009933;">Link to wiki</span></a><br>
        <br>
        -You can also watch streams of better players to get an idea of the way to play :
        <a href="https://www.twitch.tv/directory/game/Supreme%20Commander%3A%20Forged%20Alliance"><span style="color:#009933;">Link to twitch website</span></a><br>
        <br>
        -You can also watch these youtube video which will help you improve :
        <a href="https://www.youtube.com/channel/UCJYYaFbqPqbNkvgJAqrhC2A/videos"><span style="color:#009933;">Link to Heaven youtube videos</span></a><br>
        <br>
        -Some trainers are also available to help you improve on the game, so don't hesitate to contact them at all !<br>
        You can ask for one in #aeolus or  in #newbie channel or find a name to contact on this topic :<br>
        <a href ="http://forums.faforever.com/viewtopic.php?f=2&t=1614"><span style="color:#009933;">Your Personal Trainer Team</span></a></center>''')

        # Achievements
        self.achievement1_image_label_tutorials.setPixmap(
            QtGui.QPixmap('res/tutorials/icons/achievement_bronze.png'))
        self.achievement2_image_label_tutorials.setPixmap(
            QtGui.QPixmap('res/tutorials/icons/achievement_bronze.png'))
        self.achievement3_image_label_tutorials.setPixmap(
            QtGui.QPixmap('res/tutorials/icons/achievement_bronze.png'))
        self.achievement4_image_label_tutorials.setPixmap(
            QtGui.QPixmap('res/tutorials/icons/achievement_bronze.png'))
        self.achievement5_image_label_tutorials.setPixmap(
            QtGui.QPixmap('res/tutorials/icons/achievement_bronze.png'))
        self.achievement6_image_label_tutorials.setPixmap(
            QtGui.QPixmap('res/tutorials/icons/achievement_bronze.png'))

        self.achievement1_progressBar_tutorials.setMinimum(0)
        self.achievement2_progressBar_tutorials.setMinimum(0)
        self.achievement3_progressBar_tutorials.setMinimum(0)
        self.achievement4_progressBar_tutorials.setMinimum(0)
        self.achievement5_progressBar_tutorials.setMinimum(0)
        self.achievement6_progressBar_tutorials.setMinimum(0)

        self.achievement1_text_label_tutorials.setText('Play 10 games')
        self.achievement1_progressBar_tutorials.setMaximum(10)
        self.achievement1_progressBar_tutorials.setValue(
            int(self.client.achievements.get_value('number_games_played')))

        self.achievement2_text_label_tutorials.setText(
            'Play 3 different tutorial maps')
        self.achievement2_progressBar_tutorials.setMaximum(3)
        number_scenario_played = len(
            (self.client.achievements.get_value('tutorial_scenario_played')).split(';'))
        if number_scenario_played > 2:
            number_scenario_played = 2
        self.achievement2_progressBar_tutorials.setValue(
            number_scenario_played)

        self.achievement3_text_label_tutorials.setText(
            'Play on 10 different maps')
        self.achievement3_progressBar_tutorials.setMaximum(10)
        self.achievement3_progressBar_tutorials.setValue(8)  # TODO

        self.achievement4_text_label_tutorials.setText('Play 2 challenge maps')
        self.achievement4_progressBar_tutorials.setMaximum(2)
        self.achievement4_progressBar_tutorials.setValue(1)  # TODO

        self.achievement5_text_label_tutorials.setText('Play 5 ladder games')
        self.achievement5_progressBar_tutorials.setMaximum(5)
        self.achievement5_progressBar_tutorials.setValue(4)  # TODO

        self.achievement6_text_label_tutorials.setText('Win 3 custom games')
        self.achievement6_progressBar_tutorials.setMaximum(3)
        self.achievement6_progressBar_tutorials.setValue(0)  # TODO


        logger.info("Tutorials instantiated.")

    def calling_for_personal_trainer(self):
        self.client.chat.join('#newbie')
        popup_message = 'You asked for a personal trainer ! Go to the "chat lobby" tab, then "#newbie" channel to see if there is one available'
        QMessageBox.about(self, 'Call for a personal trainer', popup_message)

        # have to send message after popup because otherwise it won't be fast enough and it can happen that there is no #newbie yet
        if '#newbie' in self.client.chat.channels:
            self.client.chat.channels['#newbie'].chatEdit.setText('Any personal trainer available ?') # need to be same message for the notification system for personal trainer
            self.client.chat.channels['#newbie'].sendLine('#newbie')



    def next_video(self):
        if self.current_index_of_video_list < len(self.video_list) - 1:
            self.current_index_of_video_list += 1
            self.show_video(self.current_index_of_video_list)
        else:
            pass

    def previous_video(self):
        if self.current_index_of_video_list > 0:
            self.current_index_of_video_list -= 1
            self.show_video(self.current_index_of_video_list)

        else:
            pass

    def start_tutorial(self, button_number):
        real_index_of_video = self.current_index_of_maps_tutorials_list[
            self.current_categorie] + button_number
        self.client.achievements.update_scenario_maps(
            'tutorial_scenario_played', self.maps_tutorial_list[self.current_categorie][real_index_of_video].map_name)
        self.client.start_tutorial_map(
            self.maps_tutorial_list[self.current_categorie][real_index_of_video].map_name)

    def start_challenge(self, button_number):
        real_index_of_video = self.current_index_of_maps_challenge_list[
            self.current_challenge_categorie] + button_number
        '''TODO :
        self.client.achievements.update_scenario_maps(
            'tutorial_scenario_played', self.maps_tutorial_list[self.current_challenge_categorie][real_index_of_video].map_name)'''
        self.client.start_tutorial_map(
            self.maps_challenge_list[self.current_challenge_categorie][real_index_of_video].map_name)

