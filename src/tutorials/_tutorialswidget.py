from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from fa.replay import replay
import util
import os
import fa

import logging
logger = logging.getLogger(__name__)
FormClass, BaseClass = util.THEME.loadUiType("tutorials/tutorials.ui")


class TutorialsWidget(FormClass, BaseClass):
    def __init__(self, client, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.client = client
        util.THEME.setStyleSheet(self, "tutorials/formatters/style.css")
        #util.THEME.setStyleSheet(self, "tournaments/formatters/style.css")

        self.label_image_video1.setPixmap(QtGui.QPixmap('res/tutorials/TopTipsFAF.png'))
        self.label_text_video1.insertHtml('''<center>
        The best tips to improve on forged alliance.<br>
        <a href='https://www.youtube.com/watch?v=Qhrz0rZmnLU'><span style="color:#009933;">Link to video</span></a>
        </center>''')

        self.label_image_video2.setPixmap(QtGui.QPixmap('res/tutorials/ClientPresentation.png'))
        self.label_text_video2.insertHtml('''<center>
        Guide on how to use the client.<br>
        <a href='https://www.youtube.com/watch?v=tqCs0WVGT_I'><span style="color:#009933;">Link to video</span></a>
        </center>''')

        self.tutorial_main_text_browser.insertHtml('''<center>
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

        self.tutorial_tutorialsmaps_text_browser.insertHtml('''<center>
        (todo)Here you will find some scenario which come from speed2 idea
        </center>''')

        self.tutorial_achievements_text_browser.insertHtml('''<center>
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
