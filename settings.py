from os import environ

SESSION_CONFIGS = [
    dict(
         name='G1',#Loss/Gain Frame
         app_sequence=['G1'],
         num_demo_participants=3,
     ),
    dict(
        name='G2',#Coord mean of transportation
        app_sequence=['G2'],
        num_demo_participants=12,
    ),
        dict(
        name='G3',#IG with comp
        app_sequence=['G3'],
        num_demo_participants=6,
    ),
        dict(
        name='G4',#
        app_sequence=['G4'],
        num_demo_participants=2,
    ),
        dict(
        name='G5',#
        app_sequence=['G5'],
        num_demo_participants=6,
    ),
        dict(
        name='G6',#
        app_sequence=['G6'],
        num_demo_participants=8,
    ),
]



# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'ECU'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3858109742357'
