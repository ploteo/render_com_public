from otree.api import *
import random
from random import sample 

doc = """
Your app description
! Not clear the return rate
"""


class C(BaseConstants):
    NAME_IN_URL = 'G5'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 9


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
  
    # assign roles to players
    for p in subsession.get_players():
        investments = ["LL","MM","HH"] #random order of the 3 images
        random.shuffle(investments)
        pictures_1 = ["G5/images/noise_1.png","G5/images/noise_2.png","G5/images/noise_3.png"] #first block of 3 images
        random.shuffle(pictures_1)
        pictures_2 = ["G5/images/noise_4.png","G5/images/noise_5.png","G5/images/noise_6.png"] #second block of 3 images
        random.shuffle(pictures_2)
        pictures_3 = ["G5/images/noise_7.png","G5/images/noise_8.png","G5/images/noise_9.png"] #third block of 3 images
        random.shuffle(pictures_3)

        #define stage
        if p.id_in_subsession % 3 == 0:
            p.treatment = "neutral"
        if p.id_in_subsession % 3 == 1:
            p.treatment = "positive"
        if p.id_in_subsession % 3 == 2:
            p.treatment = "negative"
        #random order at the individual level
        if p.round_number == 1:
            p.participant.vars['investments'] = investments # to store the order

            if p.treatment != "neutral": # to insert the treatment figure
                pictures_1[0]="G5/images/"+p.treatment+"_"+investments[0]+".png"
                random.shuffle(pictures_1)
                #print(pictures_1)
                pictures_2[0]="G5/images/"+p.treatment+"_"+investments[1]+".png"
                random.shuffle(pictures_2)
                pictures_3[0]="G5/images/"+p.treatment+"_"+investments[2]+".png"
                random.shuffle(pictures_3)
            p.participant.vars['pictures'] = [pictures_1]
            p.participant.vars['pictures'].append(pictures_2)
            p.participant.vars['pictures'].append(pictures_3)
            #print(p.participant.vars['pictures'])

        
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.CharField()
    image = models.CharField()
    check = models.CharField(
        choices=["True","False"],
        widget=widgets.RadioSelect
    )
    investment = models.CurrencyField(choices=[0,20,40,60,80,100], widget=widgets.RadioSelectHorizontal)   
    investment_type = models.CharField()
    survey_1  = models.CharField(choices=["Not at all risky","A little risky","Moderately risky","Very risky","Extremely risky"], widget=widgets.RadioSelectHorizontal)
    survey_2  = models.CharField(choices=["Not at all risky","A little risky","Moderately risky","Very risky","Extremely risky"], widget=widgets.RadioSelectHorizontal)        
    survey_3  = models.CharField(choices=["Not at all risky","A little risky","Moderately risky","Very risky","Extremely risky"], widget=widgets.RadioSelectHorizontal)


# PAGES
class Display(Page): #first image in block of 3
    form_model = 'player'
    form_fields = ['check']
    @staticmethod
    def vars_for_template(player):
        if player.round_number <=3:
            image =  player.participant.vars['pictures'][0][player.round_number-1][10:-4]
            image_path = player.participant.vars['pictures'][0][player.round_number-1]
        if player.round_number >3 and player.round_number <=6:
            image =  player.participant.vars['pictures'][1][player.round_number-4][10:-4]
            image_path = player.participant.vars['pictures'][1][player.round_number-4]
        if player.round_number >6:
            image =  player.participant.vars['pictures'][2][player.round_number-7][10:-4]
            image_path = player.participant.vars['pictures'][2][player.round_number-7]

        player.image = image #to save the image name in the database

        questions = {
            "noise_1":"The most popular name for girls has been Princess Butter.",
            "noise_2":"The newfound breed of butterfly has been called Morpho amazonicus.",
            "noise_3":"The film tells the story of a small-business office clerk.",
            "noise_4":"The two characters named in the article are Neon Nova and Galactic Hologram.",
            "noise_5":"Roger Federer won the match.",
            "noise_6":"The cooking hack involves the use of a blender.",
            "noise_7":"The film promises a riveting blend of suspense and emotion.",
            "noise_8":"The students cited in the article come from the Faculty of Law of the University of Trento.",
            "noise_9":"The breakup involved famous celebrities Luna Stone and Max Sterling.",
            "positive_LL":"Investors assure a strong post-pandemic forecast.",
            "positive_MM":"Smart home devices are not a part of the industry’s growth.",
            "positive_HH":"Optimism in the industry has come from treatments and vaccines.",
            "negative_LL":"Uncertainty in the market has been brought by crumbling foreign investment.",
            "negative_MM":"Oversaturation is not a key component of the industry’s decline.",
            "negative_HH":"Investors are questioning the short-term viability of Biotech Startups."
        }
        #find the right questions
        question = questions[image]
        print(question)
        return {
            'image_path': image_path,
            'question': question,
        }
        

class Investment(Page): 
    form_model = 'player'
    form_fields = ['investment']

    def vars_for_template(player):
        if player.round_number == 3:
            player.investment_type = player.participant.vars['investments'][0]
        if player.round_number == 6:
            player.investment_type = player.participant.vars['investments'][1]
        if player.round_number == 9:
            player.investment_type = player.participant.vars['investments'][2]
        return {
            'investment_type': player.investment_type,
        }

    def is_displayed(player: Player):
        return player.round_number == 3 or player.round_number == 6 or player.round_number == 9
 
class Investment_outcome(Page): 

                      
    def vars_for_template(player):
        random_number = random.randint(1,100)

        if player.investment_type == "LL":
            if random_number <= 60:
                win = True
                player.payoff = player.investment * (2) + (100- player.investment)*1.04
            else:
                win = False
                player.payoff = player.investment * (0) + (100- player.investment)*1.04
        
        if player.investment_type == "MM":
            if random_number <= 50:
                win = True
                player.payoff = player.investment * (2) + (100- player.investment)*1.04
            else:
                win = False
                player.payoff = player.investment * (0) + (100- player.investment)*1.04

        if player.investment_type == "HH":
            if random_number <= 40:
                win = True
                player.payoff = player.investment * (8) + (100- player.investment)*1.04
            else:
                player.payoff = player.investment * (8) + (100- player.investment)*1.04
                win = False
        return {
            'win': win
        }

    def is_displayed(player: Player):
        return player.round_number == 3 or player.round_number == 6 or player.round_number == 9
 

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    def vars_for_template(player):
        hist = player.in_all_rounds()
        payoffs = [p.payoff for p in hist]
        tot_payoffs = sum(payoffs)
        return {
            'tot_payoffs': tot_payoffs,
        }
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS #only show in first round

class Survey(Page):
    form_model = 'player'
    form_fields = ['survey_1', 'survey_2', 'survey_3']

    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS #only show in first round

page_sequence = [Display, Investment, Investment_outcome, Results, Survey]
