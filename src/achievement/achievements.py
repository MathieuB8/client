import logging
logger = logging.getLogger(__name__)
from config import Settings
import util
from PyQt5.QtWidgets import QMessageBox

class Achievements():
    def remove_all_none_achievements(self):
        if self.get_value('number_games_played') is None:
            self.update_value('number_games_played', 0)
        if self.get_value('tutorial_scenario_maps_played') is None:
            self.update_value('tutorial_scenario_maps_played', '')


        if self.get_value('maps_played') is None:
            self.update_value('maps_played', '')
        if self.get_value('maps_challenge_played') is None:
            self.update_value('maps_challenge_played', '')
        if self.get_value('number_ladder_games') is None:
            self.update_value('number_ladder_games', 0)
        if self.get_value('called_a_trainer') is None:
            self.update_value('called_a_trainer', 0)

    def debug_reset_achievements(self):
        self.update_value('number_ladder_games', 0)
        self.update_value('number_games_played', 0)
        self.update_value('called_a_trainer', 0)
        self.update_value('maps_challenge_played', '')
        self.update_value('maps_played', '')
        self.update_value('tutorial_scenario_maps_played', '')

    def show_value_all_achievements(self):
        logger.info ('Achievements 10 games>>'+str(self.get_value('number_games_played')))
        QMessageBox.about(None, "number_games_played achievmeents", str(self.get_value('number_games_played')))

        logger.info ('Achievements number_ladder_games>>'+str(self.get_value('number_ladder_games')))
        QMessageBox.about(None, "number_ladder_games ", str(self.get_value('number_ladder_games')))

        logger.info ('Achievements maps_challenge_played>>'+str(self.get_value('maps_challenge_played')))
        QMessageBox.about(None, "maps_challenge_played achievmeents", str(self.get_value('maps_challenge_played')))

        logger.info ('Achievements maps_played>>'+str(self.get_value('maps_played')))
        QMessageBox.about(None, "maps_played ", str(self.get_value('maps_played')))

        logger.info ('Achievements tutorial_scenario_maps_played>>'+str(self.get_value('tutorial_scenario_maps_played')))
        QMessageBox.about(None, "tutorial_scenario_maps_played achievmeents", str(self.get_value('tutorial_scenario_maps_played')))

        logger.info ('Achievements called_a_trainer>>'+str(self.get_value('called_a_trainer')))
        QMessageBox.about(None, "called_a_trainer achievmeents", str(self.get_value('called_a_trainer')))


    def __init__(self, client, *args, **kwargs):
        self.client = client
        Settings.persisted_property('achievement/number_games_played', type=int, default_value = 0)
        Settings.persisted_property('achievement/tutorial_scenario_maps_played', type=str, default_value = '')

        Settings.persisted_property('achievement/maps_played', type=str, default_value = '')
        Settings.persisted_property('achievement/maps_challenge_played', type=str, default_value='')
        Settings.persisted_property('achievement/number_ladder_games', type=int, default_value = 0)
        Settings.persisted_property('achievement/called_a_trainer', type=int, default_value = 0)

        self.remove_all_none_achievements()

        #        self.debug_reset_achievements()
        # debug :        self.show_value_all_achievements()
        logger.info('Achievement initialised')

    def update_all_maps_games_achievement(self, game_length, featured_mod, mapname):
        if game_length > 4 * 60 : #otherwise they can just spam maps...
            if featured_mod == 'faf':
                new_number_games_played = 1+int(self.get_value('number_games_played'))
                self.update_value('number_games_played',new_number_games_played)
                if new_number_games_played <= self.client.tutorials.achievement1_max_number:
                    self.client.tutorials.update_progress_bar('number_games_played', new_number_games_played)
            elif featured_mod == 'ladder1v1':
                new_number_ladder_games_played = 1+int(self.get_value('number_ladder_games'))
                self.update_value('number_ladder_games', new_number_ladder_games_played)
                if new_number_ladder_games_played <= self.client.tutorials.achievement5_max_number:
                    self.client.tutorials.update_progress_bar('number_ladder_games', new_number_ladder_games_played)
            if mapname != 'tutorialtab_map': # doesn't take into acount scenario/challenge maps of tutorial tab
                self.update_list_maps('maps_played',str(mapname))

    def update_value(self, name, value):
        util.settings.setValue('achievement/' + name, value)

    def update_list_maps(self, name, mapname): # used by tutorial scenario maps and challenge maps
        current_value_achievement = self.get_value(name)
        if mapname not in current_value_achievement and current_value_achievement.count(";") < 20: # to avoid having a string too long, just limit it the goal of the achievement, TODO change this number/!\
            updated_maps_list = current_value_achievement + ";" + str(mapname)
            self.update_value(name, updated_maps_list)

            number_different_maps_played = updated_maps_list.count(";")
            self.client.tutorials.update_progress_bar(name, number_different_maps_played)


    def get_value(self, name):
        return Settings.get('achievement/' + name)
