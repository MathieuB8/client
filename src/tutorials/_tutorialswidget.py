from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from fa.replay import replay
import util
import os
import fa
from PyQt5.QtGui import QIcon, QPixmap
from tutorials.tutorialsytvideo import TutorialsVideo
from tutorials.maptutorial import MapTutorial


import logging
logger = logging.getLogger(__name__)
FormClass, BaseClass = util.THEME.loadUiType("tutorials/tutorials.ui")


class TutorialsWidget(FormClass, BaseClass):

    video_list = []
    maps_tutorial_list =[]
    current_index_of_video_list = 0
    current_index_of_maps_tutorials_list = 1

    def setup_initial_videos(self):
        initialvideo=TutorialsVideo('https://www.youtube.com/embed/Qhrz0rZmnLU','The best tips to improve on forged alliance.')
        self.video_list.append(initialvideo)
        video2=TutorialsVideo('https://www.youtube.com/embed/tqCs0WVGT_I','Guide on how to use the client.')
        self.video_list.append(video2)

        self.show_video(self.current_index_of_video_list)

    def setup_initial_maps_tutorial(self):
        self.map1_pushbutton_tutorials.setFlat(True)
        self.map2_pushbutton_tutorials.setFlat(True)
        self.map3_pushbutton_tutorials.setFlat(True)
        map=MapTutorial('res/tutorials/map1.png','FAF_TUT_Theta_BO')
        self.maps_tutorial_list.append(map)
        map2=MapTutorial('res/tutorials/map2.png','FAF_TUT_FourLeaf_BO')
        self.maps_tutorial_list.append(map2)
        map3=MapTutorial('res/tutorials/map3.png','FAF_TUT_Loki_BO')
        self.maps_tutorial_list.append(map3)
        map4=MapTutorial('res/tutorials/map4.png','FAF_TUT_SummerDuel_BO')
        self.maps_tutorial_list.append(map4)
        map5=MapTutorial('res/tutorials/map5.png','FAF_TUT_Loki_BO')
        self.maps_tutorial_list.append(map5)
        map6=MapTutorial('res/tutorials/map6.png','FAF_TUT_Theta_BO')
        self.maps_tutorial_list.append(map6)
        self.set_stylesheet_for_maps(1)

    def set_stylesheet_for_maps(self,index):
        if 1 <= self.current_index_of_maps_tutorials_list <= len(self.maps_tutorial_list)-2:
            logger.info('previous map zawa22>>' +str(self.current_index_of_maps_tutorials_list))
            self.map1_pushbutton_tutorials.setStyleSheet('border-image: url('+str(self.maps_tutorial_list[index-1].link)+');');
            self.map2_pushbutton_tutorials.setStyleSheet('border-image: url('+str(self.maps_tutorial_list[index].link)+');');
            self.map3_pushbutton_tutorials.setStyleSheet('border-image: url('+str(self.maps_tutorial_list[index+1].link)+');');

    def update_maps_images(self):
        logger.info('update called >>>>' +str(self.current_index_of_maps_tutorials_list))
        if 1 <= self.current_index_of_maps_tutorials_list <= len(self.maps_tutorial_list)-2:
            logger.info('previous map zawa>>>>' +str(self.current_index_of_maps_tutorials_list))
            self.set_stylesheet_for_maps(self.current_index_of_maps_tutorials_list)

    def previous_map(self):
        if  self.current_index_of_maps_tutorials_list > 1:
            self.current_index_of_maps_tutorials_list-=1
            self.update_maps_images()

    def next_map(self):
        logger.info('NEXT MAP CLICKED with the index '+str(self.current_index_of_maps_tutorials_list))
        if self.current_index_of_maps_tutorials_list < len(self.maps_tutorial_list)-2:
            logger.info('GG NEXT MAP CLICKED with the index '+str(self.current_index_of_maps_tutorials_list))
            self.current_index_of_maps_tutorials_list+=1
            self.update_maps_images()

    def show_video(self,index_of_video):
        if 0<=index_of_video<len(self.video_list):
            self.video_webengine_tutorials.setUrl(self.video_list[index_of_video].link)
            self.description_video_textBrowser_tutorials.setHtml('''<center>
            ''' + self.video_list[index_of_video].description + '''
            </center>''')

    def __init__(self, client, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.client = client
        util.THEME.setStyleSheet(self, "tutorials/formatters/style.css")
        self.setup_initial_videos()
        self.setup_initial_maps_tutorial()

        self.nextvideo_pushbutton_tutorials.clicked.connect(self.next_video)
        self.previousvideo_pushbutton_tutorials.clicked.connect(self.previous_video)


        self.previousmap_pushbutton_tutorials.clicked.connect(self.previous_map)
        self.nextmap_pushbutton_tutorials.clicked.connect(self.next_map)
        self.map1_pushbutton_tutorials.clicked.connect(lambda: self.start_tutorial(-1))
        self.map2_pushbutton_tutorials.clicked.connect(lambda: self.start_tutorial(0))
        self.map3_pushbutton_tutorials.clicked.connect(lambda: self.start_tutorial(1))

    def next_video(self):
        if self.current_index_of_video_list < len(self.video_list) - 1 :
            self.current_index_of_video_list+=1
            self.show_video(self.current_index_of_video_list)
        else:
            pass

    def previous_video(self):
        if self.current_index_of_video_list > 0 :
            self.current_index_of_video_list-=1
            self.show_video(self.current_index_of_video_list)

        else:
            pass


    def start_tutorial(self,button_number):
        real_index_of_video = self.current_index_of_maps_tutorials_list + button_number
        self.client.start_tutorial_map_zawa(self.maps_tutorial_list[real_index_of_video].map_name)

    def backup(self):

        self.label_image_video2.setPixmap(QtGui.QPixmap('res/tutorials/ClientPresentation.png'))
        self.label_text_video2.setHtml('''<center>
        Guide on how to use the client.<br>
        <a href='https://www.youtube.com/watch?v=tqCs0WVGT_I'><span style="color:#009933;">Link to video</span></a>
        </center>''')

        self.tutorial_main_text_browser.setHtml('''<center>
        Welcome to forged alliance forever ! If you want ever more information about this game you can check these tutorials in order to improve :<br>
        <a href='https://wiki.faforever.com/index.php?title=Main_Page'><span style="color:#009933;">Link to wiki</span></a><br>
        <br>
        You can also watch streams of better players to get an idea of the way to play :<br>
        <a href="https://www.twitch.tv/directory/game/Supreme%20Commander%3A%20Forged%20Alliance"><span style="color:#009933;">Link to twitch website</span></a><br>
        <br><br>
        You can also watch these youtube video which will help you improve :<br>
        <a href=https://www.youtube.com/channel/UCJYYaFbqPqbNkvgJAqrhC2A/videos"><span style="color:#009933;">Link to Heaven youtube videos</span></a><br>
        <br><br>
        Some trainers are also available to help you improve on the game, so don't hesitate to contact them at all !<br>
        You can ask for one in #aeolus or  in #newbie channel or find a name to contact on this topic :<br>
        <a href ="http://forums.faforever.com/viewtopic.php?f=2&t=1614"><span style="color:#009933;">Your Personal Trainer Team</span></a><br>
        <span style="color:#009933;">(todo, not working)Call for a personal trainer</span>
        </center>''')

        self.tutorial_tutorialsmaps_text_browser.setHtml('''<center>
        (todo)Here you will find some scenario which come from speed2 idea
        </center>''')

        self.tutorial_achievements_text_browser.setHtml('''<center>
        (todo)Achievements :<br>
        [] : Play 10 different maps on custom games<br>
        [] : Get trained by a trainer<br>
        [] : Reach 600 global rating<br>
        [] : Play 10 games on ladder<br>
        [] : Reach 500 ladder rating<br>
        [] : Play 30 different maps on custom games<br>
        [] : Reach 1000 global rating<br>
        [] : Reach 1000 ladder rating<br>
        </center>''')


        logger.info("Tutorials instantiated.")
