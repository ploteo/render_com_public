from otree.api import *
import csv
from datetime import date, timedelta

doc = """
- Agent
    - IMPORT outcome Day 1 for Day 2
"""

# IMPORT PAYOFFS ROUND 1

# with open('agent_welcome/input_agent.csv', encoding='utf-8') as file:
#     read = list(csv.DictReader(file))
#     print(read)

class C(BaseConstants):
    NAME_IN_URL = 'welcome'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = __name__ + "/instructions.html"

    TIMEOUT_1 = 180 #duration of the task
    TIMEOUT_2 = 90 #duration of the task
    PIECE_RATE = cu(.1) #earnings for each problem solved
    EARN_BEL=cu(1)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    type=models.CharField()
    performance_1 = models.IntegerField()
    hired= models.CharField()
    prolific_id = models.CharField()

# PAGES

class Introduction(Page):
    @staticmethod # this need to be fixed
    def vars_for_template(player: Player):
        #retrieve prolific ID
        player.prolific_id = player.participant.prolific_id
        # display times
        today = date.today()
        tomorrow= today + timedelta(days=1)

        day = player.subsession.session.config['day']
        return{
            'today': today.strftime("%B %d, %Y"),
            'tomorrow': tomorrow.strftime("%B %d, %Y"),
            'day': day    
            }

class Outcome(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (player.subsession.session.config['day'] == 2)

    @staticmethod # 
    def vars_for_template(player: Player):
        if player.subsession.session.config['day'] == 2:

            with open('agent_welcome/input_agent.csv', encoding='utf-8') as file:
                read = list(csv.DictReader(file))
                print(read)

            for i in read:
                    if str(i["prolific_id"]) == str(player.participant.prolific_id):
                        player.performance_1=int(i["performance"])
                        player.hired=i["hired"]
                        break
                    else:
                        pass

        return {
            'hired': 'Hired' if player.hired=="yes" else 'Not hired',
            'performance':  player.performance_1
        }

page_sequence = [Introduction, Outcome]
