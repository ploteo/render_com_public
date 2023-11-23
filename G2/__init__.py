from otree.api import *


doc = """
A coordination game with 4 players (transportation mode)
Two types of players: A and B
- treatment is the matching of A and B

"""


class C(BaseConstants):
    NAME_IN_URL = 'G2'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1

    ENDOWMENT = cu(30)
    THRESHOLD = 13

    CAR_COST = 30
    BUS_COST = 10
    BIKE_COST= 0

    CAR_EMISSIONS = 7
    BUS_EMISSIONS = 3
    BIKE_EMISSIONS = 0

    CAR_UTILITY = 140
    BUS_UTILITY = 100
    BIKE_UTILITY = 80


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    n_bike = models.IntegerField()
    n_bus = models.IntegerField()
    n_car = models.IntegerField()
    total_emissions = models.IntegerField()
    threshold_break = models.BooleanField()
    car_utility = models.FloatField()
    bus_utility = models.FloatField()
    bike_utility = models.FloatField()


class Player(BasePlayer):
    treatment = models.CharField()
    type=models.CharField()
    choice=models.CharField(
    choices=[
            ["Car", 'Car'],
            ["Bus", 'Bus'],
            ["Bike", 'Bike']],
            widget=widgets.RadioSelect,
            label="What is your preferred mode of transportation?"
    )
    living_standards = models.IntegerField(
        choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neither Agree nor Disagree'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
            )
    goods_services = models.IntegerField(        
        choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neither Agree nor Disagree'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
            )
    taxes = models.IntegerField(        
        choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neither Agree nor Disagree'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
            )
    comforts = models.IntegerField(
        choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neither Agree nor Disagree'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
            )
    own_behavior = models.IntegerField(
        choices=[
            [0, 'Strongly Disagree'],
            [1, 'Disagree'],
            [2, 'Neither Agree nor Disagree'],
            [3, 'Agree'],
            [4, 'Strongly Agree']],
            widget=widgets.RadioSelectHorizontal
            )
    feelings = models.IntegerField(
        choices=[
            [0, 'Very concerned'],
            [1, 'Somewhat concerned'],
            [2, 'No opinion'],
            [3, 'Not concerned'],
            [4, 'Not at all concerned']],
            widget=widgets.RadioSelectHorizontal
            )
    wtp = models.IntegerField(
        choices=[
            [0, '0%'],
            [1, '0%-10%'],
            [2, '10%-20%'],
            [3, '20%-40%'],
            [4, '40+%']],
            widget=widgets.RadioSelectHorizontal
            )
    transportation_change = models.IntegerField(
        choices=[
            [0, 'Not at all'],
            [1, 'Unlikely'],
            [2, 'Maybe, it depends'],
            [3, 'To some extent'],
            [4, 'Definitely']],
            widget=widgets.RadioSelectHorizontal
            )

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:  # this way we get a fixed role across repetitions
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)
    # assign treatments
    for p in subsession.get_players():
        if p.group_id % 7 == 1:
            p.treatment="ctrl1"
            p.type="A"

        if p.group_id % 7 == 2:
            p.treatment="ctrl2"
            p.type="B"

        if p.group_id % 7 == 3:
            p.treatment="trtm1"
            if p.id_in_group < 4:
                p.type="A"
            else:
                p.type="B"

        if p.group_id % 7 == 4 or p.group_id % 7 == 5 or p.group_id % 7 == 6:
            p.treatment="trtm2"
            if p.id_in_group == 1 or p.id_in_group == 2:
                p.type="A"
            else: 
                p.type="B"
                
        if p.group_id % 7 == 0:
            p.treatment="trtm3"
            if p.id_in_group == 1:
                p.type="A"
            else: 
                p.type="B"     

def set_payoffs(group: Group):
    players = group.get_players()
    for p in players:
        if p.choice == "Car":
            p.payoff = C.ENDOWMENT - C.CAR_COST + C.CAR_UTILITY
        if p.choice == "Bus":
            p.payoff = C.ENDOWMENT - C.BUS_COST + C.BUS_UTILITY
        if p.choice == "Bike":
            p.payoff = C.ENDOWMENT - C.BIKE_COST + C.BIKE_UTILITY

    choices = [p.choice for p in players]
    print(choices)
    # count the number of each choice
    group.n_car = choices.count("Car")
    group.n_bus = choices.count("Bus")
    group.n_bike = choices.count("Bike")
    # calculate total emissions
    emissions = []
    for i in choices:
        if i == "Car":
            emissions.append(C.CAR_EMISSIONS)
        if i == "Bus":
            emissions.append(C.BUS_EMISSIONS)
        if i == "Bike":
            emissions.append(C.BIKE_EMISSIONS)
    # do they break the emission cap?
    group.total_emissions = sum(emissions)
    if group.round_number >1:
        if group.total_emissions > C.THRESHOLD:
            group.car_utility = (group.in_round(group.round_number - 1).car_utility - .15*(group.total_emissions-C.THRESHOLD))
            group.bus_utility = (group.in_round(group.round_number - 1).bus_utility - .15*(group.total_emissions-C.THRESHOLD))
            group.bike_utility = (group.in_round(group.round_number - 1).bike_utility - .15*(group.total_emissions-C.THRESHOLD))
            group.threshold_break = True
        else:
            group.car_utility = group.in_round(group.round_number - 1).car_utility
            group.bus_utility = group.in_round(group.round_number - 1).bus_utility
            group.bike_utility = group.in_round(group.round_number - 1).bike_utility
            group.threshold_break = False
    else: 
        if group.total_emissions > C.THRESHOLD:
            group.car_utility =  C.CAR_UTILITY - .15*(group.total_emissions-C.THRESHOLD)
            group.bus_utility =  C.BUS_UTILITY - .15*(group.total_emissions-C.THRESHOLD)
            group.bike_utility = C.BIKE_UTILITY - .15*(group.total_emissions-C.THRESHOLD)
            group.threshold_break = True
        else:
            group.car_utility =  C.CAR_UTILITY
            group.bus_utility = C.BUS_UTILITY
            group.bike_utility = C.BIKE_UTILITY
            group.threshold_break = False
        
   

#     for p in group.get_players():
#         if p.choice == "Car":
#             p.payoff = 0
#         if p.choice == "Bus":
#             p.payoff = 1
#         if p.choice == "Bike":
#             p.payoff = 2


# PAGES
class StartPage(Page):
    def is_displayed(player: Player):
        return player.round_number == 1 #only show in first round

class ChoicePage(Page):
    form_model = 'player'
    form_fields = ['choice']

    def vars_for_template(player: Player):
        if player.round_number==1:
            car_utility = C.CAR_UTILITY
            bus_utility = C.BUS_UTILITY
            bike_utility = C.BIKE_UTILITY
        else:
            car_utility = player.in_round(player.round_number - 1).group.car_utility
            bus_utility = player.in_round(player.round_number - 1).group.bus_utility
            bike_utility = player.in_round(player.round_number - 1).group.bike_utility
        return {
            'car_utility': car_utility,
            'bus_utility': bus_utility,
            'bike_utility': bike_utility,
        }

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'
    # see method 'set_payoffs' in class Group in models.py
    # payoffs are computed here


class Results(Page):
    def vars_for_template(player: Player):
        return{
            'threshold_break': player.group.threshold_break,
            'total_emissions': player.group.total_emissions,
            'n_car': player.group.n_car,
            'n_bus': player.group.n_bus,
            'n_bike': player.group.n_bike
        }
    
class FinalResults(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS #only show in first round
    
    def vars_for_template(player: Player):
        hist = player.in_all_rounds()
        tot_payoffs = sum([g.payoff for g in hist])
        return{
            'tot_payoffs': tot_payoffs
        }
    
class Survey(Page):
    form_model = 'player'
    form_fields = ['living_standards', 'goods_services', 'taxes', 'comforts', 'own_behavior', 'feelings', 'wtp', 'transportation_change']

    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS #only show in first round
    

page_sequence = [StartPage, ChoicePage, ResultsWaitPage, Results, FinalResults, Survey]
