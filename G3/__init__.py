from otree.api import *
import random
from operator import itemgetter

doc = """
AN IG repeated 3 times in 3 different stages
Stage 1: Ctrl
Stage 2: Tournament
Stage 3: Tournament + Money



! why investment must be positive?
! something wrong in the rewrd function: give a fixed amiunt
"""


class C(BaseConstants):
    NAME_IN_URL = 'G3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 9
    ENDOWMENT = 100
    #parameters of IG
    IG_A_gain = 2
    IG_A_loss = 1
    IG_A_gain_prob = 75
    IG_B_gain_prob = 50
    IG_C_gain_prob = 25
    IG_B_gain = 4
    IG_B_loss = .5
    IG_C_gain = 10
    IG_C_loss = 0
    CONV_RATE=.35



class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    # assign treatments
    for p in subsession.get_players():
        p.participant.label= "CL"+str(p.participant.id_in_session)
        if p.round_number <= 3:
            p.treatment = 'ctrl'
        elif p.round_number > 3 and p.round_number <= 6:
            p.treatment = 'tournament'
        else:
            p.treatment = 'money'




class Group(BaseGroup):
    first_ID = models.CharField()
    first_earnings = models.FloatField()
    second_ID = models.CharField()
    second_earnings = models.FloatField()
    third_ID = models.CharField()
    third_earnings = models.FloatField()

def investment_return(group: Group):
    drawn = random.randint(1,100)
    players = group.get_players()
    for p in players:
        if p.investment_profile == "A":
            if drawn <= C.IG_A_gain_prob:
                p.payoff = (C.ENDOWMENT-p.investment)+C.IG_A_gain*p.investment
            else:
                p.payoff = (C.ENDOWMENT-p.investment)+C.IG_A_loss*p.investment
        elif p.investment_profile == "B":
            if drawn <= C.IG_B_gain_prob:
                p.payoff = (C.ENDOWMENT-p.investment)+C.IG_B_gain*p.investment
            else:
                p.payoff = (C.ENDOWMENT-p.investment)+C.IG_B_loss*p.investment
        else:
            if drawn <= C.IG_C_gain_prob:
                p.payoff = (C.ENDOWMENT-p.investment)+C.IG_C_gain*p.investment
            else:
                p.payoff = (C.ENDOWMENT-p.investment)+C.IG_C_loss*p.investment

    all_gains=[]
    for p in players:
        all_gains.append([p.participant.label, p.payoff]) #replace id_in_group with player.label (id_in_group)
    all_gains_sorted = sorted(all_gains, key=itemgetter(1),reverse=True)
    # find their position int he ranking and assign them money if treatment is money
    for p in players:
        p.rank = all_gains_sorted.index([p.participant.label, p.payoff])+1
        if p.treatment == 'money':
            if p.rank == 1:
                p.payoff_plus = float(p.payoff) + float(p.investment*0.015)
            elif p.rank == 2:
                p.payoff_plus = float(p.payoff) + float(p.investment*0.01)
            elif p.rank == 3:
                 p.payoff_plus = float(p.payoff) + float(p.investment*0.005)
            else:
                p.payoff_plus = float(p.payoff)
        else:
            p.payoff_plus = float(p.payoff)

    #to store them in the group
    group.first_ID = all_gains_sorted[0][0]
    group.first_earnings = float(all_gains_sorted[0][1])
    group.second_ID = all_gains_sorted[1][0]
    group.second_earnings = float(all_gains_sorted[1][1])
    group.third_ID = all_gains_sorted[2][0]
    group.third_earnings = float(all_gains_sorted[2][1])


class Player(BasePlayer):
    treatment = models.CharField()
    investment = models.IntegerField(min=1, max=100)
    investment_profile = models.CharField()
    payoff_plus = models.FloatField()
    rank = models.IntegerField()
    ctrl_1 = models.CharField(choices=[
            ["A", 'A) Yes'],
            ["B", 'B) No']
            ],
            widget=widgets.RadioSelect
            )
    ctrl_2 =  models.CharField(choices=[
            ["A", 'A) The sum of rounds\' payoff'],
            ["B", 'B) The payoff obtained in a randomly elicited round']
            ],
            widget=widgets.RadioSelect
            )
    ctrl_3 = models.IntegerField()
    fin_lit_1  = models.CharField(choices=[
            ["A", 'More than $102'],
            ["B", 'Exactly $102'],
            ["C", 'Less than $102'],
            ["D", 'Don\'t know'],
            ["E", 'Refuse to answer'],
            ],
            widget=widgets.RadioSelect
            )
    fin_lit_2  = models.CharField(choices=[
            ["A", 'More than today'],
            ["B", 'Exactly the same as today'],
            ["C", 'Less than today'],
            ["D", 'Don\'t know'],
            ["E", 'Refuse to answer'],
            ],
            widget=widgets.RadioSelect
            )
    fin_lit_3  = models.CharField(choices=[
            ["A", 'True'],
            ["B", 'False'],
            ["C", 'Don\'t know'],
            ["D", 'Refuse to answer']
            ],
            widget=widgets.RadioSelect
            )

# PAGES
class StartPage(Page):
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Control(Page):
    form_model = 'player'
    form_fields = ['ctrl_1', 'ctrl_2', 'ctrl_3']

    def is_displayed(player: Player):
        return player.round_number == 1
    
    def error_message(player, values):
        if values["ctrl_1"] != "B":
            return 'Incorrect answer to Q1'
        elif values["ctrl_2"] != "B":
          return 'Incorrect answer to Q2'
        elif values["ctrl_3"] != 100:
            return 'Incorrect answer to Q3'
        
class Instr_phase1(Page):
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Instr_phase2(Page):
    def is_displayed(player: Player):
        return player.round_number == 4
    
class Instr_phase3(Page):
    def is_displayed(player: Player):
        return player.round_number == 7
         
class Investment(Page):
    form_model = 'player'
    form_fields = ['investment', 'investment_profile']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'investment_return'


class Results(Page):
    def vars_for_template(player: Player):
        if player.treatment == 'money':
            bonus = round(float(player.payoff_plus) - float(player.payoff),2)
        else:
            bonus = 0
        return {
            'own_rank': player.rank,
            'own_gains': player.payoff,
            'bonus': bonus,
            'first_ID': player.group.first_ID,
            'first_earnings': player.group.first_earnings,
            'second_ID': player.group.second_ID,
            'second_earnings': player.group.second_earnings,
            'third_ID': player.group.third_ID,
            'third_earnings': player.group.third_earnings
        }
class Survey(Page):
    form_model = 'player'
    form_fields = ['fin_lit_1', 'fin_lit_2','fin_lit_3']
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    


class FinalResults(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    def vars_for_template(player: Player):
        round_1= random.randint(1,3)
        round_2= random.randint(4,6)
        round_3= random.randint(7,9)

        hist = player.in_all_rounds()
        all_payoffs = [g.payoff for g in hist]
        payoff_1 = all_payoffs[int(round_1-1)]
        payoff_2 = all_payoffs[int(round_2-1)]
        payoff_3 = all_payoffs[int(round_3-1)]

        tot_payoffs = payoff_1+payoff_2+payoff_3

        return{
            'round_1': round_1,
            'round_2': round_2,
            'round_3': round_3,
            'tot_payoffs': tot_payoffs
        }


page_sequence = [StartPage,  Control, Instr_phase1, Instr_phase2, Instr_phase3, Investment, ResultsWaitPage, Results, Survey, FinalResults]
