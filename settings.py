from os import environ

#this is for block 1
import random

#print(sequence)

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

LANGUAGE_CODE = 'en' # <- CHANGE GERE: it,en

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.00,
    'participation_fee': 0.00,
    'doc': ""
}
# e.g. EUR, GBP, CNY, JPY

REAL_WORLD_CURRENCY_CODE = 'EUR' 
USE_POINTS = False
POINTS_CUSTOM_NAME = 'Tokens'

SESSION_CONFIGS = [ 
    dict(
        name="MAIN_Agent_1",
        display_name="Agent Day 1",
        num_demo_participants=6,
        app_sequence=["prolific_id", "agent_welcome", "agent_task"],
        day=1  # day = 1 they work first day; day = 2 they also get feedback about earnings in day 1
    ),
    dict(
        name="MAIN_Agent_2",
        display_name="Agent Day 2",
        num_demo_participants=6,
        app_sequence=["prolific_id", "agent_welcome", "agent_task"],
        day=2  # day = 1 they work first day; day = 2 they also get feedback about earnings in day 1
    ),
    dict(
        name="MAIN_Principal",
        display_name="Principal",
        num_demo_participants=3,
        app_sequence=["prolific_id", "principal_hiring"]
    )
        #    dict(name = 'Beauty_ITA',
        # app_sequence = ['beauty_contest_ITA'],
        # num_demo_participants= 3
        # )
]

PARTICIPANT_FIELDS = ['returns', 'timeout','prolific_id', 'performance']


ROOMS = [
    dict(name='live_demo_1', display_name='Room for live 1 (no participant labels)'),
	 dict(name='live_demo_2', display_name='Room for live 2 (no participant labels)'),
 dict(
        name='econ_lab_secure',
        display_name='Experimental Economics Lab 40s (secure)',
        participant_label_file='_rooms/labels.txt',
	    use_secure_urls=True
    ),
     dict(
        name='econ_lab',
        display_name='Experimental Economics Lab 40s',
        participant_label_file='_rooms/labels.txt',
	    use_secure_urls=False
    )
    ]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# don't share this with anybody.
SECRET_KEY = 'h5qahzqsl#mi1=ahzqq!9-qhkf8d$m7go8lol*+uw2$9s&=_tw'

INSTALLED_APPS = ['otree','otreeutils']

OTREE_AUTH_LEVEL = 'DEMO'
