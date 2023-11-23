from otree.api import *

doc = """
Conflict od interest in financial advisor
TODO: Need to implement final computations
! what to do with those who are not well-behaved? I would have used EG

"""


class C(BaseConstants):
    NAME_IN_URL = 'G4'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
    A_h = 2.00
    A_l = 1.60
    B_h = 3.85
    B_l = 0.10

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    # assign roles to players
    for p in subsession.get_players():
        #define stage
        if p.round_number <= 2:
            p.stage = 2
        else:
            p.stage = 3
        if p.id_in_group % 2 == 0:
            p.type="advisor"
        else:
            p.type="client"

class Group(BaseGroup):
    investment_profile = models.CharField()
    investment_accept = models.BooleanField(choices=[
            [True, 'Accept'],
            [False, 'Reject']
            ],
            widget=widgets.RadioSelect)
    client_risk_profile = models.CharField()


class Player(BasePlayer):
    stage = models.IntegerField()
    type = models.CharField()
    HL_1 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
                            )
    HL_2 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_3 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_4 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_5 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_6 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_7 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_8 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_9 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    HL_10 = models.CharField(
        choices=['A', 'B'], widget=widgets.RadioSelectHorizontal
    )
    risk_profile = models.CharField()
 
def risk_profile(group: Group):
    # calculate risk profile
    if group.round_number == 1:
        for player in group.get_players():
            choices = [player.HL_1, player.HL_2, player.HL_3, player.HL_4, player.HL_5, player.HL_6, player.HL_7, player.HL_8, player.HL_9, player.HL_10]
            print(choices)
            print(choices.count("A"))
            if choices.count("A") <= 3:
                player.risk_profile = "risk seeker"
            else:
                player.risk_profile = "risk averse"
            if player.type == "client": # write to group the client's risk profile
                group.client_risk_profile = player.risk_profile


# PAGES
class StartPage(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class PageHL(Page):
    form_model = 'player'
    form_fields = [
        'HL_1',
        'HL_2',
        'HL_3',
        'HL_4',
        'HL_5',
        'HL_6',
        'HL_7',
        'HL_8',
        'HL_9',
        'HL_10',
    ]  # all 10 options
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        # retrieve values from constants and store them in a dictionary
        return {'A_h': C.A_h, 'A_l': C.A_l, 'B_h': C.B_h, 'B_l': C.B_l}

class Role(Page):
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Info(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class StageInfo(Page):
    def is_displayed(player: Player):
        return player.round_number == 1 or player.round_number == 3
    
class TaskAdvisor(Page):
    form_model = 'group'
    form_fields = ['investment_profile']
    @staticmethod
    def is_displayed(player: Player):
        return player.type == "advisor"
    @staticmethod
    def vars_for_template(player: Player):
        # retrieve profile from first round
        group_profile= player.group.in_round(1)
        client_profile= group_profile.client_risk_profile
        return {
            'client_risk_profile': client_profile
        }

class TaskClient_1(Page):
    
    def is_displayed(player: Player):
        return player.type == "client" and (player.round_number == 1 or player.round_number == 3)

    def vars_for_template(player: Player):
        return {
            'advisor_choice': player.group.investment_profile
        }

class TaskClient_2(Page):
    form_model = 'group'
    form_fields = ['investment_accept']
    
    def is_displayed(player: Player):
        return  player.type == "client" and (player.round_number == 2 or player.round_number == 4)

    def vars_for_template(player: Player):
        return {
            'advisor_choice': player.group.investment_profile
        }

class ChoiceWaitPage(WaitPage):
    pass

class RiskWaitPage(WaitPage):
    after_all_players_arrive = risk_profile


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [StartPage, PageHL, RiskWaitPage, Role, Info, StageInfo, TaskAdvisor, ChoiceWaitPage, TaskClient_1, TaskClient_2, ResultsWaitPage, Results]
