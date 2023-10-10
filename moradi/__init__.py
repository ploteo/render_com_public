from otree.api import *
from operator import itemgetter
import csv
import random


author = 'MP'

doc = """
WE RETRIEVE VALUES FROM THE FILE to DISPLAY IT
"""

# IMPORT PERFORMANCES  ROUND 1 
with open('moradi/cap_placenames_it_ger_tolomei.csv', encoding='utf-8') as file:
    read = list(csv.DictReader(file))
    #print(read)


class C(BaseConstants):
    NAME_IN_URL = 'ethnicity'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

   # list of municipalities for the drop down menu in the background questionnaire 
    MUNICIPALITY=[]
    for i in read:
        MUNICIPALITY.append(str(i['mun_german']))
    MUNICIPALITY=list(dict.fromkeys(MUNICIPALITY))# remove duplicates
    MUNICIPALITY=sorted(MUNICIPALITY, key=itemgetter(0))#sort

    TEXTS = ["Wie stark fühlen Sie sich diesen geografischen Gruppen zugehörig?",
             "2",
             "3",
             "4",
             "5"
            ] # here the text of the question (match with the answer)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participation = models.BooleanField(
        choices=[[1,"Ja, ich möchte an dieser Studie teilnehmen und bestätige, dass ich in Südtirol geboren wurde."],[0,"Nein, ich möchte nicht teilnehmen."]],
        widget=widgets.RadioSelect,
        label="")
    
    gender = models.CharField(choices=[
            ["Male", 'Männlich'],
            ["Female", 'Weiblich']],
    widget=widgets.RadioSelect
    )
    age = models.IntegerField(choices = [[1,"20-24"],[2,"25-29"], [3,"30-34"], [4,"35-39"], [5,"40-44"],[6,"45-49"],[7,"50-54"],[8,"55-59"],[9,"60-64"],[10,"65-69"],[11,"70-74"], [12,"+74"]] ,label="",widget=widgets.RadioSelectHorizontal)# why in ranges
      # resident
    residence = models.CharField(choices=C.MUNICIPALITY, label="")
    # grew up
    grew_up = models.CharField(choices=C.MUNICIPALITY, label="")
    weiler = models.CharField(choices=["Ja","Nein"],widget=widgets.RadioSelectHorizontal, label="")
    fraktion = models.CharField(choices=["Ja","Nein"],widget=widgets.RadioSelectHorizontal, label="")
  
    mother_tongue = models.CharField(choices=["Deutsch","Italienisch","Ladin","Andere (bitte nennen) "],widget=widgets.RadioSelectHorizontal, label="")
    #----------------------------------
    #SELF-IDENTIFICATION (Page 1)
    #----------------------------------
    Q1_1 = models.CharField() #fraktion or weiler
    Q1_2 = models.CharField()
    Q1_3 = models.CharField()
    Q1_4 = models.CharField()
    Q1_5 = models.CharField()
    Q1_6 = models.CharField()
    Q1_7 = models.CharField()
    Q1_8 = models.CharField()
    Q1_9 = models.CharField()
    #----------------------------------
    Q2_1 = models.CharField() 
    Q2_2 = models.CharField()
    Q2_3 = models.CharField()
    Q2_4 = models.CharField() 
    Q2_5 = models.CharField()
    Q2_6 = models.CharField()
    Q2_7 = models.CharField() 
    Q2_8 = models.CharField()
    Q2_9 = models.CharField()
#----------------------------------
    Q3_1 = models.CharField()
    Q3_2 = models.CharField()
    Q3_3 = models.CharField()
    Q3_4 = models.CharField()
    Q3_5 = models.CharField()
    Q3_6 = models.CharField()
    #----------------------------------
    #END SELF-IDENTIFICATION
    #----------------------------------
    #----------------------------------
    #REMEMBRANCE CULTURE (Pge 2)
    #----------------------------------
    Q4_1 = models.CharField()
    Q4_2 = models.CharField()
    Q4_3 = models.CharField()
    Q4_4 = models.CharField()
    Q4_5 = models.CharField()
    Q4_6 = models.CharField()
#----------------------------------
    Q5_1 = models.CharField()
#----------------------------------
    Q6_1 = models.CharField()
    Q6_2 = models.CharField()
    Q6_3 = models.CharField()
    Q6_4 = models.CharField()
    Q6_free =  models.StringField(blank=True)
#----------------------------------
    Q7_1 = models.CharField()    
    Q7_2 = models.CharField()
    Q7_3 = models.CharField()
    Q7_4 = models.CharField()
    Q7_5 = models.CharField()
    Q7_6 = models.CharField()
    Q7_7 = models.CharField()
    Q7_8 = models.CharField()
    Q7_9 = models.CharField()
    Q7_10 = models.CharField()
    Q7_free =  models.StringField(blank=True)
    #----------------------------------
    #END REMEMBRANCE CULTURE
    #----------------------------------
    # VALUE OF HISTORY (Page 3)
    #----------------------------------
    Q8_1 = models.CharField()
    Q8_2 = models.CharField()
    Q8_3 = models.CharField()
    Q8_4 = models.CharField()
    Q8_5 = models.CharField()
    #----------------------------------
    Q9_1 = models.CharField()
    #----------------------------------
    Q10_1 = models.CharField()
    #----------------------------------
    Q11_1 = models.CharField()
    #----------------------------------
    #END VALUE OF HISTORY
    #----------------------------------

    #----------------------------------
    # PLACES
    #----------------------------------

    QP_1 = models.CharField()
    QP_2 = models.CharField()
    QP_3 = models.CharField()
    QP_4 = models.CharField()
    QP_5 = models.CharField()
    QP_6 = models.CharField()
    QP_7 = models.CharField()

# FUNCTIONS

def creating_session(subsession):
    #----------------------------------
    # select relevant info
    info = []
    for i in read:
        info.append([str(i['mun_german']),str(i["plz"]), str(i["loc_german"],), str(i["loc_italian"]), int(i["ctolomei2"])])
    #print(info)
    # assign 5 random places to each subject (we will ad a place form their birthplace later)
    for p in subsession.get_players():
        p.participant.places = [random.sample(info,9)]
        #print(p.participant.places)

# k is the question number, i is the answer number, j is the value of the answer
def make_input(k,i,j):
    name="Q"+str(k)+"_"+str(i+1)
    id = "id_Q"+str(k)+"_"+str(i+1)
    return f""" 
    <label>
        <input type=\"radio\" id=\"{id}\" name=\"{name}\" value=\"{j}\">
    </label>
    """

#custom export
class locations(ExtraModel):
    player = models.Link(Player)
    places = [] #models.CharField()

def custom_export(players):
    # Export the ExtraModel as a CSV file
    yield ['session.code', 'participant.code', 'places'] 
    # 'filter' without any args returns everything
    loc = locations.filter()
    for l in loc:
        player = l.player
        participant = player.participant
        session = player.session
        places = player.participant.places
        yield [session.code, participant.code, places]

#----------------------------------
# PAGES
#----------------------------------
class WaitPage(WaitPage):
    pass

class Intro(Page):
    form_model = 'player'
    form_fields = ['participation']

    def is_displayed(player):
        return player.round_number == 1
    
class Background(Page):
    form_model = 'player'
    form_fields = ['age','gender','residence','grew_up','weiler','fraktion','mother_tongue']

    def before_next_page(player, timeout_happened):
        player.participant.places = []
        info = []
        info_1 = []
        for i in read:
            info.append([str(i['mun_german']),str(i["plz"]), str(i["loc_german"],), str(i["loc_italian"]), int(i["ctolomei2"])])
            if i.get('mun_german') == player.grew_up:
                info_1.append([str(i['mun_german']),str(i["plz"]), str(i["loc_german"],), str(i["loc_italian"]), int(i["ctolomei2"])])
        draw = random.sample(info,9) # randm draw 9 places
        draw_1 = random.sample(info_1,1) # random draw own place
        draw.append(draw_1[0])
        random.shuffle(draw)
        player.participant.places.append(draw) # need to save the list somewhere

        locations.create(player=player,  places=player.participant.places) # to write the extradata
    
class Page_1(Page):
    form_model = 'player'
    def get_form_fields(player):
        list=[]
        #----------------------------------
        # Q1
        #----------------------------------
        if player.fraktion == "Ja" and player.weiler == "Ja":
            for i in range(1,10):
                list.append("Q1_"+str(i))
        if player.fraktion == "Ja" and player.weiler == "Nein":
            for i in range(1,9):
                list.append("Q1_"+str(i))
        if player.fraktion == "Nein" and player.weiler == "Ja":
            for i in range(1,9):
                list.append("Q1_"+str(i))
        if player.fraktion == "Nein" and player.weiler == "Nein":
            for i in range(1,8):
                list.append("Q1_"+str(i))
        #----------------------------------
        # Q2
        #----------------------------------
        if player.fraktion == "Ja" and player.weiler == "Ja":
            for i in range(1,10):
                list.append("Q2_"+str(i))
        if player.fraktion == "Ja" and player.weiler == "Nein":
            for i in range(1,9):
                list.append("Q2_"+str(i))
        if player.fraktion == "Nein" and player.weiler == "Ja":
            for i in range(1,9):
                list.append("Q2_"+str(i))
        if player.fraktion == "Nein" and player.weiler == "Nein":
            for i in range(1,8):
                list.append("Q2_"+str(i))
#----------------------------------
        for i in range(1,7):
            list.append("Q3_"+str(i))
        return list
    
    def is_displayed(player):
        player_1 = player.in_round(1)
        return player_1.participation == 1

    @staticmethod
    def vars_for_template(player):
        #----------------------------------
        # Q1 
        #----------------------------------
        # condition Q1 to the answer given in the background questionnaire
        if player.fraktion == "Ja" and player.weiler == "Nein":
            q = [
                "A.	Fraktion, in der Sie leben",
                "B.	Ort, in der Sie leben",
                "C.	Gemeinde, in der Sie leben",
                "D.	Südtirol",
                "E.	Euregio (Südtirol, Tirol, Trentino)",
                "F.	Italien",
                "G.	Europa",
                "H.	Die Welt als Ganzes"]
        if player.weiler == "Ja" and player.fraktion == "Nein":
            q= [
                "A.	Weiler, in der Sie leben",
                "B.	Ort, in der Sie leben",
                "C.	Gemeinde, in der Sie leben",
                "D.	Südtirol",
                "E.	Euregio (Südtirol, Tirol, Trentino)",
                "F.	Italien",
                "G.	Europa",
                "H.	Die Welt als Ganzes"]
        if player.weiler == "Ja" and player.fraktion == "Ja":
            q= [
                "A.	Fraktion, in der Sie leben",
                "B.	Weiler, in der Sie leben",
                "C.	Ort, in der Sie leben",
                "D.	Gemeinde, in der Sie leben",
                "E.	Südtirol",
                "F.	Euregio (Südtirol, Tirol, Trentino)",
                "G.	Italien",
                "H.	Europa",
                "I.	Die Welt als Ganzes"]   
        if player.fraktion == "Nein" and player.weiler == "Nein":
            q = [
                "A.	Ort, in der Sie leben",
                "B.	Gemeinde, in der Sie leben",
                "C.	Südtirol",
                "D.	Euregio (Südtirol, Tirol, Trentino)",
                "E.	Italien",
                "F.	Europa",
                "G.	Die Welt als Ganzes"]
                
        # prepare the display
        k=1 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_1=tab

        #------------------------------------
        # end Q1
        #------------------------------------

        #------------------------------------
        #Q2
        #------------------------------------
         # condition Q1 to the answer given in the background questionnaire
        if player.fraktion == "Ja" and player.weiler == "Nein":
            q = [
                "A. Fraktion",
                "B. Ort",
                "C. Gemeinde",
                "D. Südtirol",
                "E. Italien",
                "F. Menschen, die dieselbe Sprache sprechen wie ich.",
                "G.	Menschen, die die gleichen religiösen Überzeugungen haben wie ich.",
                "H.	Menschen, die derselben ethnischen Gruppe angehören wie ich."]
        if player.weiler == "Ja" and player.fraktion == "Nein":
            q= ["A. Weiler",
                "B. Ort",
                "C. Gemeinde",
                "D. Südtirol",
                "E. Italien",
                "F. Menschen, die dieselbe Sprache sprechen wie ich.",
                "G.	Menschen, die die gleichen religiösen Überzeugungen haben wie ich.",
                "H.	Menschen, die derselben ethnischen Gruppe angehören wie ich."]
        if player.weiler == "Ja" and player.fraktion == "Ja":
            q= ["A. Weiler",
                "B. Fraktion",
                "C. Ort",
                "D. Gemeinde",
                "E. Südtirol",
                "F. Italien",
                "G. Menschen, die dieselbe Sprache sprechen wie ich.",
                "H.	Menschen, die die gleichen religiösen Überzeugungen haben wie ich.",
                "I.	Menschen, die derselben ethnischen Gruppe angehören wie ich."]   
        if player.fraktion == "Nein" and player.weiler == "Nein":
            q = ["A. Ort",
                "B. Gemeinde",
                "C. Südtirol",
                "D. Italien",
                "E. Menschen, die dieselbe Sprache sprechen wie ich.",
                "F.	Menschen, die die gleichen religiösen Überzeugungen haben wie ich.",
                "G.	Menschen, die derselben ethnischen Gruppe angehören wie ich."]


 # prepare the display
        k=2 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_2=tab
        #------------------------------------
        # end Q2
        #------------------------------------
        #------------------------------------
        #Q3
        #------------------------------------
        q = ["A. Insgesamt wird meine Gruppe von anderen positiv gesehen.",
            "B. Ich fühle mich gut/stolz/froh, Mitglied meiner Gruppe zu sein.",
            "C. Wenn jemand meine Gruppe kritisiert, fühlt es sich wie eine persönliche Beleidigung an.",
            "D. Was mit meiner Gruppe passiert, wird Auswirkungen auf mein Leben haben.",
            "E. Ich nehme an Aktivitäten teil, die meine Gruppe unterstützen.",
            "F. Ich bin mir der Traditionen und der Geschichte meiner Gruppe bewusst."
            ]
# prepare the display
        k=3 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_3=tab      

        return {'tab_1':tab_1,
                'tab_2':tab_2,
                'tab_3':tab_3,
                }

class Page_2(Page):
    form_model = 'player'
    form_fields = ['Q4_1','Q4_2','Q4_3','Q4_4','Q4_5','Q4_6','Q5_1','Q6_1','Q6_2','Q6_3','Q6_4','Q6_free','Q7_1','Q7_2','Q7_3','Q7_4','Q7_5','Q7_6','Q7_7','Q7_8','Q7_9','Q7_10','Q7_free']

    def is_displayed(player):
        player_1 = player.in_round(1)
        return player_1.participation == 1

    @staticmethod
    def vars_for_template(player):
        q = ["A. Ritualisiertes Gedenken an einem bestimmten historischen Tag (z.B. Andreas-Hofer-Gedenktag, Tag der Autonomie, Corona Gedenktag)",
            "B.	Denkmäler",
            "C.	Mahnmale",
            "D.	Historische Museen",
            "E.	Ortschronisten",
            "F.	Geschichtsunterricht in der Schule"]
        
        k=4 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_4=tab    

        q = [""]
        k=5 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_5=tab  


        q = ["A. Ende des 1. Weltkrieges (1918)",
             "B. Annexion Südtirols (1920)",
             "C. Option (1939)",
             "D. Abschluss des 2. Autonomiestatuts (1992)"] #omitted anderes
            
        k=6 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_6=tab    

        q = ["<a href=\"https://de.wikipedia.org/wiki/Ötzi\" target=\"_blank\"> A. Ötzi</a>",
             "<a href=\"https://de.wikipedia.org/wiki/Andreas_Hofer\" target=\"_blank\"> B. Andreas Hofer</a>",
                "<a href=\"https://de.wikipedia.org/wiki/Katharina_Lanz\" target=\"_blank\">C. Katharina Lanz</a>",
                  "<a href=\"https://de.wikipedia.org/wiki/Sepp_Innerkofler\" target=\"_blank\">D. Sepp Innerkofler </a>",
                   "<a href=\"https://de.wikipedia.org/wiki/Ettore_Tolomei\" target=\"_blank\">E. Ettore Tolomei </a>",
                    "<a href=\"https://de.wikipedia.org/wiki/Edwina_Aberham\" target=\"_blank\">F. Edwina Aberham</a>",
                     "<a href=\"https://de.wikipedia.org/wiki/Hans_Kammerlander\" target=\"_blank\"> G. Hans Kammerlander</a>",
                      "<a href=\"https://de.wikipedia.org/wiki/Angela_Nikoletti\" target=\"_blank\">H. Angela Nikoletti </a>",
                         "I. Elisabeth Kofler-Langer",
                         "<a href=\" https://de.wikipedia.org/wiki/Dorothea_Agetle\" target=\"_blank\">J. Dorothea Agetle </a>",
                        
             ] #omitted anderes
            
        k=7 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th style="min-width:120px"></th><th style="min-width:40px">1</th><th style="min-width:40px">	2</th><th style="min-width:40px">3</th><th style="min-width:40px">4</th><th style="min-width:40px">5</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_7=tab    
        
        
        return {'tab_4':tab_4,
                'tab_5': tab_5,
                'tab_6': tab_6,
                'tab_7': tab_7
        }
    
class Page_3(Page):
    form_model = 'player'
    form_fields = ['Q8_1','Q8_2','Q8_3','Q8_4','Q8_5']

    def is_displayed(player):
        player_1 = player.in_round(1)
        return player_1.participation == 1

    @staticmethod
    def vars_for_template(player):
        q = ["A. Geschichte besteht hauptsächlich aus Verbrechen.",
            "B.	Geschichte wird tagtäglich erlebt, gesungen, getanzt, erfahren.",
            "C.	Geschichte ist identitätsstiftend.",
            "D.	Geschichte trennt.",
            "E.	Man sollte Geschichte Geschichte sein lassen."]
  
        k=8 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th align ="left"></th><th>Stimme überhaupt nicht zu </th><th> Stimme nicht zu</th><th>Stimme weder zu noch nicht zu </th><th>Stimme zu </th><th>  Stimme völlig zu</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_8=tab   

        q=[""]
        k=9 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th align ="left"></th><th>Stimme überhaupt nicht zu </th><th> Stimme nicht zu</th><th>Stimme weder zu noch nicht zu </th><th>Stimme zu </th><th>  Stimme völlig zu</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_9=tab   

        q=[""]
        k=10 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th align ="left"></th><th>Stimme überhaupt nicht zu </th><th> Stimme nicht zu</th><th>Stimme weder zu noch nicht zu </th><th>Stimme zu </th><th>  Stimme völlig zu</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_10=tab   

        q=[""]
        k=11 # the index of the question
        tab ='<table class="table">'
        tab+= '<i> <tr><th align ="left"></th><th>Stimme überhaupt nicht zu </th><th> Stimme nicht zu</th><th>Stimme weder zu noch nicht zu </th><th>Stimme zu </th><th>  Stimme völlig zu</th></tr></i>'
        for i in range(0,len(q)): 
            tab+= '<tr><td align ="left">'
            tab+= str(q[i])
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'
        tab_11=tab   


        return {'tab_8':tab_8,
                'tab_9': tab_9,
                'tab_10': tab_10,
                'tab_11': tab_11
        }
     

class Places(Page):
    # form_model = 'player'
    # form_fields = ['gender']

    def is_displayed(player):
        player.round_number == C.NUM_ROUNDS
        player_1 = player.in_round(1)
        return player_1.participation == 1

 
    @staticmethod
    def vars_for_template(player):

        # prepare the display
        k="P" # the index of the question
        tab ='<table class="table">'
        tab+= '<i><SPAN STYLE="font-size:10pt"> </i><br>'
        tab+= '<tr><th align ="left">Ortsname A</th>'
        tab+= '<th align ="left">Ortsname B</th><th>1 </th><th> 2</th><th>3 </th><th>4 </th><th>  5</th></tr>'
        for i in range(0,10): 
            tab+= '<tr>'
            tab+='<td>'
            tab+= player.participant.places[0][i][2]
            tab+='</td>'
            tab+='<td>'
            tab+= player.participant.places[0][i][3]
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,1)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,2)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,3)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,4)
            tab+='</td>'
            tab+='<td align ="center">'
            tab+= make_input(k,i,5)
            tab+='</td>'
            tab+='</tr>'
        tab+='</table>'

        

        return {'body': tab,
                }
    
#--------------------------------------------------------------

page_sequence = [Intro, Background, Page_1, Page_2, Page_3, Places]
