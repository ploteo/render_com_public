from otree.api import *
import random

doc = """
Loss gain/frame over 9 rounds. Treatment between subjects. Same order of questions for all subjects.
COMMENTS:
- Why not randomize the order of the questions?
"""


class C(BaseConstants):
    NAME_IN_URL = 'G1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 9
    CAUSES = [["MC1","DIS","ED1","AST","ELD","MC2","WOM","ED2","WIL"],
                ["The Cancer Research Foundation will be able to save many lives in the future if there are sufficient funds.", 
                 "Many lives will be saved by preparing vulnerable regions adequately for the impact of hurricanes which the Disaster Relief Group can do with your support.",
                 "With your help, a poor child can go to school leading to a promising future.",
                 "Sufficient funding secures the exploration of space ensuring the early detection of earthbound asteroids.",
                 "With your donation, local community centers can organize social activities helping elderly people that struggle with loneliness.",
                 "If you donate to MedWorldwide people in need will be supplied with vaccines resulting in fewer preventable deaths.",
                 "With your help, Fight4Rights can continue raising awareness and informing about domestic violence to reduce its occurrences.",
                 "The Outreach Project will be able to build schools and train teachers to provide a quality education in underprivileged communities with the help of your donation.",
                 "With your support, the Wildlife Conservation Fund can finance projects to save endangered species and preserve biodiversity on our planet."],
                ["The Cancer Research Foundation won’t be able to save many lives in the future if there are insufficient funds.",
                 "Many lives will be lost by not preparing vulnerable regions adequately for the impact of hurricanes which the Disaster Relief Group can not do without your support.",
                 "Without your help, a poor child cannot go to school leading to an unpromising future.",
                 "Insufficient funding threatens the exploration of space endangering the early detection of earth-bound asteroids.",
                 "Without your donation, local community centers can not organize social activities helping elderly people that struggle with loneliness.",
                 "If you do not donate to MedWorldwide people in need will not be supplied with vaccines resulting in more preventable deaths.",
                 "Without your help, Fight4Rights can not continue raising awareness and informing about domestic violence to reduce its occurrences.",
                 "The Outreach Project will not be able to build schools and train teachers to provide a quality education in underprivileged communities without the help of your donation.",
                 "Without your support, the Wildlife Conservation Fund can not finance projects to save endangered species and preserve biodiversity on our planet."
                ]  
                ] #LABELS, GAIN FRAME, LOSS FRAME


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    condition = models.CharField()
    cause = models.CharField()
    donation = models.IntegerField(min=0, max=100)
    Cvol = models.IntegerField(
    choices=[
            [0, 'Never'],
            [1, 'Rarely'],
            [2, 'Sometimes'],
            [3, 'Often'],
            [4, 'Always']],
            widget=widgets.RadioSelectHorizontal
    )
    Cdon = models.IntegerField(
    choices=[
            [0, 'Never'],
            [1, 'Rarely'],
            [2, 'Sometimes'],
            [3, 'Often'],
            [4, 'Always']],
            widget=widgets.RadioSelectHorizontal
    )
    Cemp = models.IntegerField(
    choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neutral'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
    )
    Cper = models.IntegerField(
    choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neutral'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
    )
    Ctim = models.IntegerField(
    choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neutral'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
    )
    Cfut = models.IntegerField(
    choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neutral'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
    )

                 



def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        if p.id_in_subsession % 2 == 0:
            p.condition="gain"
        else:
            p.condition="loss"

# PAGES
class Instructions(Page):
    def is_displayed(player: Player):
        return player.round_number == 1 #only show in first round
    
class Donation(Page):
    form_model = 'player'
    form_fields = ['donation']
    def vars_for_template(player: Player):
        player.cause=C.CAUSES[0][player.round_number-1]

        card="<div class=\"card\">"
        card+="<div class=\"card-body\">"
        if player.condition=="gain":
            card+="<p>"+C.CAUSES[1][player.round_number-1]+"</p>"
        else:
            card+="<p>"+C.CAUSES[2][player.round_number-1]+"</p>"
        card+="</div>"
        card+="</div>"

        return dict(
            card=card
        )

class Survey(Page):
    form_model = 'player'
    form_fields = ['Cvol','Cdon','Cemp','Cper','Ctim','Cfut']
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS #only show in last round
    
class Results(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS #only show in last round

    def vars_for_template(player: Player):
        round_chosen=int(random.sample(range(1,10),1)[0])
        if player.condition=="gain":
            cause=C.CAUSES[1][round_chosen-1]
        else:
            cause=C.CAUSES[2][round_chosen-1] 
        donation = player.in_round(round_chosen).donation
        
        return dict(
            donation=donation,
            remainder=100-donation,
            remainder_EURO=round((100-donation)*0.1,1),
            cause=cause
        )


page_sequence = [Instructions, Donation, Survey, Results]
