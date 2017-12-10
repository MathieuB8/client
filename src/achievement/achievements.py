import logging
logger = logging.getLogger(__name__)
from config import Settings
import util
from PyQt5.QtWidgets import QMessageBox

class Achievements():

    def reset_all_achievements(self):
        self.update_value('10gamesplayed', 0)

    def show_value_all_achievements(self):
        logger.info ('Achievements 10 games>>'+str(self.get_value('10gamesplayed')))
        QMessageBox.about(None, "10games achievmeents", str(self.get_value('10gamesplayed')))


    def __init__(self, *args, **kwargs):
        Settings.persisted_property('achievement/10gamesplayed', type=int, default_value=0)



        self.show_value_all_achievements()
        logger.info('Achievement initialised')

    def update_value(self, name, value):
        util.settings.setValue('achievement/' + name, value)

    def get_value(self, name):
        return Settings.get('achievement/' + name)
