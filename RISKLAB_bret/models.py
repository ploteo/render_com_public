from otree.api import (
	models,
	widgets,
	BaseConstants,
	BaseSubsession,
	BaseGroup,
	BasePlayer,
	Currency as c,
	currency_range,
	ExtraModel
)

import random
import math
import json
from otree.api import safe_json
import itertools

author = 'Mittone Tam'

doc = """

"""


class Constants(BaseConstants):
	name_in_url = 'tam_bret'
	players_per_group = None
	num_rounds = 1

	# BRET
	box_value = 1
	num_rows = 8
	num_cols = 4
	box_height = '80px'
	box_width = '90px'
	random_payoff = True
	instructions = True
	feedback = True
	results = True
	dynamic = False
	time_interval = 1.00
	random = True
	devils_game = False
	undoable = True

	exchange_rate = 0.1



# ******************************************************************************************************************** #
# *** SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):
	pass




# ******************************************************************************************************************** #
# *** GROUP
# ******************************************************************************************************************** #

class Group(BaseGroup):
	pass
# ******************************************************************************************************************** #
# *** PLAYER
# ******************************************************************************************************************** #

class Player(BasePlayer):

	# BRET
	bomb = models.IntegerField()
	bomb_location = models.TextField()
	boxes_collected = models.IntegerField()
	boxes_scheme = models.TextField()
	round_to_pay = models.IntegerField()
	round_result = models.CurrencyField(initial=0)
	pay_bret = models.IntegerField(initial=0)

	# PARTE BRET

	def set_payoff(self):
		if self.bomb == 0:
			self.round_result = c(self.boxes_collected * Constants.box_value* Constants.exchange_rate)
		else:
			self.round_result = c(0)
		self.participant.vars['pay_bret'] = self.round_result
		# self.payoff = self.payoff + self.round_result

	# --- store values as global variables for session-wide use
	def set_globals(self):
		self.participant.vars['bomb'] = [p.bomb for p in self.in_all_rounds()]
		self.participant.vars['bomb_location'] = [p.bomb_location for p in self.in_all_rounds()]
		self.participant.vars['boxes_collected'] = [p.boxes_collected for p in self.in_all_rounds()]
		self.participant.vars['boxes_scheme'] = [p.boxes_scheme for p in self.in_all_rounds()]
		# self.session.vars['round_result'] = [p.round_result for p in self.in_all_rounds()]
		# self.session.vars['bret_payoff'] = [p.payoff for p in self.in_all_rounds()]
		self.participant.vars['round_result'] = self.round_result
