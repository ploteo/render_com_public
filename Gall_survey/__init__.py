from otree.api import *


doc = """
This will be administered to participants and given to all groups
"""


class C(BaseConstants):
    NAME_IN_URL = 'Gall_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(choices=range(18, 99))
    gender = models.CharField(choices=["Male","Female","Non-binary","Prefer not to say"], widget=widgets.RadioSelect)
    english = models.CharField(choices=["Yes","No"], widget=widgets.RadioSelect)
    investment = models.CharField(choices=["No","I invested less than €100","I invested a sum from €100 to €1 000","I am an active investor"], widget=widgets.RadioSelect)
    news = models.CharField(choices=["No","1 or 2 I care about","Several that interest me","I read investment digests daily"], widget=widgets.RadioSelect)
    social = models.CharField(choices=["No","Only from sources I trust","Yes"], widget=widgets.RadioSelect)
    father = models.CharField(choices=["Primary or lower secondary education (e.g. elementary or middle school diploma)","Upper secondary education (e.g. high school diploma or equivalent)","Tertiary education (e.g. bachelor/master’s degree or above)"], widget=widgets.RadioSelect)
    mother = models.CharField(choices=["Primary or lower secondary education (e.g. elementary or middle school diploma)","Upper secondary education (e.g. high school diploma or equivalent)","Tertiary education (e.g. bachelor/master’s degree or above)"], widget=widgets.RadioSelect)
    area = models.CharField(choices=["An inner city area","A suburban area","A town","A village","Rural or countryside","Mixture/moved around"], widget=widgets.RadioSelect)






# PAGES
class Anag(Page):
    form_model = 'player'
    form_fields =['age','gender','english','investment','news','social','father','mother','area']
    



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Anag]
