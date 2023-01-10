from otree.api import *
import random
from operator import itemgetter
import csv

doc = """
WE RETRIEVE VALUES FROM THE PERFORMANCE AND MATCH PARTICIPANTS INTO GROUPS WHO PERFORMED SIMILARLY. 2 players worked but one is the principal and just hires

"""

# IMPORT PERFORMANCES  ROUND 1 
with open('principal_hiring/input_principal.csv', encoding='utf-8') as file:
    read = list(csv.DictReader(file))
    print(read)

class C(BaseConstants):
    NAME_IN_URL = 'hiring'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MULTIPLIER= cu(.5) # for the principal, multiplied by tasks solved correctly

    TIMEOUT_1 = 180  # duration of the task in the first round
    TIMEOUT_2 = 90  # duration of the task in the second round
    PIECE_RATE = cu(.1)  # earnings for each problem solved

    EARN_BEL = cu(1)
    LOSS_BEL = cu(0)

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    #----------------------------------
    # temporary, these data will be inputed from other app via participant.vars
    # for p in subsession.get_players():
    #     p.participant.performance = [p.id_in_subsession, random.sample(range(1,15),1)[0]]
    #     p.participant.beliefs = [p.id_in_subsession,
    #                             random.sample(range(0, 100), 1)[0]]
    #     print(p.participant.performance)
    #----------------------------------    
    #----------------------------------
    # here algo to define the matching
    #----------------------------------
    rank = []
    for i in read:
        rank.append([str(i["prolific_id"]), int(i["performance_1"]),
                    int(i["beliefs"]), int(i["performance_2"])])
    rank = sorted(rank, key=itemgetter(1)) # sort it for performance 1
    print(rank)
    
# WE need to assign to the principals a couple of match (list of lists)
    c = 0
    for p in subsession.get_players():
        p.participant.performance = [rank[c],rank[c+1]]
        c=c+2
        print(p.participant.performance)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    hire=models.CharField()

    prolific_id = models.CharField()

    ID_A = models.CharField()
    performance_A_1 = models.IntegerField()  #performance in round 1
    performance_A_2 = models.IntegerField() #performance in round 2
    beliefs_A = models.IntegerField()

    ID_B = models.CharField()
    performance_B_1 = models.IntegerField()  #performance in round 1
    performance_B_2 = models.IntegerField()  # performance in round 2
    beliefs_B = models.IntegerField()

    display = models.IntegerField()  # to randomize the display


# PAGES


class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == 1)

    @staticmethod
    def vars_for_template(player: Player):
        player.prolific_id = player.participant.prolific_id

        return dict(
            time = C.TIMEOUT_1 if player.round_number == 1 else C.TIMEOUT_2,
            piece_rate = C.PIECE_RATE,
        )

class Instructions(Page):
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            time = C.TIMEOUT_2,
            piece_rate = C.PIECE_RATE,
        )

class Hire(Page):
    form_model = 'player'
    form_fields = ['hire']

    @staticmethod
    def vars_for_template(player: Player): 

        player.ID_A = player.participant.performance[0][0]
        player.ID_B = player.participant.performance[1][0]
        player.performance_A_1 = player.participant.performance[0][1]
        player.performance_B_1 = player.participant.performance[1][1]
        player.beliefs_A = player.participant.performance[0][2]
        player.beliefs_B = player.participant.performance[1][2]
        player.performance_A_2 = player.participant.performance[0][3]
        player.performance_B_2 = player.participant.performance[1][3]

        # to randomize the display order:  #0 = best performer to the right; 1=best performer to the left
        player.display = random.randint(0, 1)

        return {
            'display': player.display,
            'beliefs_A': player.beliefs_A,
            'performance_A': player.performance_A_1,
            'beliefs_B': player.beliefs_B,
            'performance_B': player.performance_B_1
         }

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    def vars_for_template(player: Player):
        if player.hire == "B":
            performance = int(player.participant.performance[1][3])
        else:
            performance = int(player.participant.performance[0][3])
        player.payoff = performance*C.MULTIPLIER

# because of randomization
        if player.display == 0:
            if player.hire == "B":
                hire = "Y"
            else:
                hire = "X"
        else:
            if player.hire == "B":
                hire = "X"
            else:
                hire = "Y"

        return{
            'hire': hire,
            'performance': performance,
            'payoff' : player.payoff
        }

      
# prolific.id,payoff,hired
# 123456789123456789123456,10,yes
# 987654321987654321987654,11.5,no

page_sequence = [Introduction, Instructions, Hire, Results]
