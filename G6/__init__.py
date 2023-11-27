from otree.api import *


doc = """
Your app description

15 round divided into 3 stages of 5 rounds each
2 treatments 
partner matching
!dropped the no answer in questionnaire
! reduce group memebers to 4
! changed alpha to .5
! do not understadn the policy implementation
! I do not understand the payoff

I wil not implement the punishment after the target is not reached (tto much of achange)
"""


class C(BaseConstants):
    NAME_IN_URL = 'G6'
    PLAYERS_PER_GROUP = 4 #they wanted 5 but safer with 4
    NUM_ROUNDS = 15
    ENDOWMENT=100
    ALPHA=0.5


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:  # this way we get a fixed role across repetitions
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)
    # assign treatments
    for p in subsession.get_players():
        if p.group.id_in_subsession % 2 == 1:
            p.treatment="treatm"
        else:
            p.treatment="ctrl"

        if p.round_number < 6:#randomize the order of the stages
            if p.group.id_in_subsession % 3 == 1:
                p.stage=1
            elif p.group.id_in_subsession % 3 == 2:
                p.stage=2
            else:
                p.stage=3
        elif p.round_number < 11:
            if p.group.id_in_subsession % 3 == 1:
                p.stage=2
            elif p.group.id_in_subsession % 3 == 2:
                p.stage=3
            else:
                p.stage=1
        else:
            if p.group.id_in_subsession % 3 == 1:
                p.stage=3
            elif p.group.id_in_subsession % 3 == 2:
                p.stage=1
            else:
                p.stage=2


class Group(BaseGroup):
    donation = models.FloatField()

def set_payoffs(group: Group):
    for p in group.get_players():
        p.participant.vars['group_contributions'] = []
        p.participant.vars['group_contributions'].append(p.contribution) #first position its her/himself
        for other in group.get_players():
            if other.id_in_group != p.id_in_group:
                p.participant.vars['group_contributions'].append(other.contribution) #then the others
        p.payoff=C.ENDOWMENT-p.contribution+(sum(p.participant.vars['group_contributions'])* C.ALPHA)
        average = round(sum(p.participant.vars['group_contributions'])/C.PLAYERS_PER_GROUP,2) 
        p.target = round(average*1.25,2)
    group.donation = sum(p.participant.vars['group_contributions'])*.05

class Player(BasePlayer):
    treatment = models.CharField()
    stage = models.IntegerField()
    contribution = models.IntegerField(min=0, max=100)
    target = models.FloatField()

    Q_1 = models.CharField() #fraktion or weiler
    Q_2 = models.CharField()
    Q_3 = models.CharField()
    Q_4 = models.CharField()
    Q_5 = models.CharField()
    Q_6 = models.CharField()
    Q_7 = models.CharField()
    Q_8 = models.CharField()
    Q_9 = models.CharField()
    Q_10 = models.CharField()
    Q_11 = models.CharField()
    Q_12 = models.CharField()
    Q_12 = models.CharField()
    Q_13 = models.CharField()
    Q_14 = models.CharField()
    Q_15 = models.CharField()

# k is the question number, i is the answer number, j is the value of the answer
def make_input(i,j):
    name="Q"+"_"+str(i+1)
    id = "id_Q"+"_"+str(i+1)
    return f""" 
    <label>
        <input type=\"radio\" id=\"{id}\" name=\"{name}\" value=\"{j}\">
    </label>
    """

# PAGES

class Welcome(Page):
      
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 

class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def vars_for_template(player: Player):
    
        # reframe the rounds
        if player.round_number <6 :
            round=player.round_number
        elif player.round_number <11 and player.round_number >5:
            round=player.round_number-5
        else:
            round=player.round_number-10
        if round > 2:
            #retrieve the target
            target = player.in_round(player.round_number-1).target 

            return {"treatment":player.treatment,
                    "stage":player.stage,
                    "round":round,
                    "target": target
                    }
        else:
            return {"treatment":player.treatment,
                    "stage":player.stage,
                    "round":round
                    }


class Survey(Page):
    form_model = 'player'
    form_fields = ['Q_1','Q_2','Q_3','Q_4','Q_5','Q_6','Q_7']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def vars_for_template(player: Player):

        q = [" 1. We are approaching the limit of the number of people the earth can support.",
                "2. Humans have the right to modify the natural environment to suit their needs.",
                "3. When humans interfere with nature it often produces disastrous consequences.",
                "4. Human ingenuity will ensure that we do NOT make the earth unlivable.",
                "5. Humans are severely abusing the environment.",
                "6. The earth has plenty of natural resources if we just learn how to develop them.",
                "7. Plants and animals have as much right as humans to exist.",
                "8. The balance of nature is strong enough to cope with the impacts of modern industrial nations.",
                "9. Despite our special abilities humans are still subject to the laws of nature.",
                "10. The so-called “ecological crisis” facing humankind has been greatly exaggerated.",
                "11. The earth is like a spaceship with very limited room and resources.",
                "12. Humans are meant to rule over the rest of nature.",
                "13. The balance of nature is very delicate and easily upset.",
                "14. Humans will eventually learn enough about how nature works to be able to control it.",
                "15. If things continue on their present course, we will soon experience a major ecological catastrophe."
                ]

        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'

        return {"table":tab}


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(player):
        contrib=player.participant.vars['group_contributions'] 
        tab ='<table class="table table-bordered"><tr>&nbsp;</tr><tr>'
        for i in range(0,len(contrib)): 
            if i == 0:
                tab+= '<td align ="left"><b>'
                tab+= str(contrib[i])
                tab+='</b></td>'
            else:
                tab+= '<td align ="left">'
                tab+= str(contrib[i])
                tab+='</td>'
        tab+='</tr></table>'
        
        if player.round_number <6 :
            round=player.round_number
        elif player.round_number <11 and player.round_number >5:
            round=player.round_number-5
        else:
            round=player.round_number-10
        


        return {'round':round,
            'table':tab,
            "donation":player.group.donation
        }



page_sequence = [Welcome, Contribution,  ResultsWaitPage,Results, Survey]
