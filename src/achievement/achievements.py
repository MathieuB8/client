import logging
logger = logging.getLogger(__name__)
from config import Settings
import util
from PyQt5.QtWidgets import QMessageBox

class Achievements():

    def reset_all_achievements(self):
        self.update_value('number_games_played', 0)

    def show_value_all_achievements(self):
        logger.info ('Achievements 10 games>>'+str(self.get_value('number_games_played')))
        QMessageBox.about(None, "number_games_played achievmeents", str(self.get_value('number_games_played')))
        logger.info ('Achievements tutorial_scenario_played>>'+str(self.get_value('tutorial_scenario_played')))
        QMessageBox.about(None, "tutorial_scenario_played ", str(self.get_value('tutorial_scenario_played')))


    def __init__(self, *args, **kwargs):
        Settings.persisted_property('achievement/number_games_played', type=int, default_value=0)
        Settings.persisted_property('achievement/tutorial_scenario_played', type=str, default_value='')



        self.show_value_all_achievements()
        logger.info('Achievement initialised')

    def update_value(self, name, value):
        util.settings.setValue('achievement/' + name, value)

    def adding_value_without_erasing_string(self, name, value):
        new_value = self.get_value(name) + ";" + str(value)
        self.update_value(name, new_value)


    def get_value(self, name):
        return Settings.get('achievement/' + name)
