from otree.api import *
import csv

author = 'Matteo P.'
doc = """
To collect the ID of participants before a prolific session.
"""

class Constants(BaseConstants):
    name_in_url = 'prolific_id'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.CharField()
    code = models.CharField()
    payoff_1 = models.CurrencyField() # payoff from day 1
    type =  models.CharField()


# FUNCTIONS
# PAGES
class ProlificID(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == 1)

    @staticmethod
    def error_message(player: Player, values):
        if len(values["prolific_id"]) != 2: # the original is 24, but we use A1, A2, A3 ...
            return 'The Prolific ID you inserted is not valid'
        # if values['code'] != "XC97R":
        #     return 'The code you inserted is not correct'
        
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.prolific_id = player.prolific_id #store it


page_sequence = [ProlificID]
# fake id: 123456789123456789123456
