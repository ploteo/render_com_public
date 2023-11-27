from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants
import random
import math
import json
from otree.api import safe_json


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #
class InstructionsBret(Page):

	# only display instruction in round 1
	def is_displayed(self):
		return self.round_number == 1

	# variables for use in template
	def vars_for_template(self):
		return {
			'num_rows':             Constants.num_rows,
			'num_cols':             Constants.num_cols,
			'num_boxes':            Constants.num_rows * Constants.num_cols,
			'num_nobomb':           Constants.num_rows * Constants.num_cols - 1,
			'box_value':            Constants.box_value,
			'time_interval':        Constants.time_interval,
		}


class Bret(Page):

	# form fields on player level
	form_model = 'player'
	form_fields = [
		'bomb',
		'boxes_collected',
		'boxes_scheme',
		'bomb_location',
	]

	# set payoffs and globals
	def before_next_page(self):
		############# TOGLIERE E' PER DEBUG
		# self.player.boxes_collected = random.randint(1,100)
		self.player.participant.vars['index_2'] = self.player.boxes_collected
		self.session.vars['reset'] = True
		self.player.set_payoff()

		if self.subsession.round_number == Constants.num_rounds:
			self.player.set_globals()

	# jsonify BRET settings for Javascript application
	def vars_for_template(self):
		reset = self.session.vars.get('reset',False)
		if reset == True:
		   del self.session.vars['reset']

		input = not Constants.devils_game if not Constants.dynamic else False

		return {
			'reset':         safe_json(reset),
			'input':         safe_json(input),
			'random':        safe_json(Constants.random),
			'dynamic':       safe_json(Constants.dynamic),
			'num_rows':      safe_json(Constants.num_rows),
			'num_cols':      safe_json(Constants.num_cols),
			'feedback':      safe_json(Constants.feedback),
			'undoable':      safe_json(Constants.undoable),
			'box_width':     safe_json(Constants.box_width),
			'box_height':    safe_json(Constants.box_height),
			'time_interval': safe_json(Constants.time_interval),
		}

	def is_displayed(self):
		return self.round_number == 1


class ResultsBret(Page):

	# only display results after all rounds have been played
	def is_displayed(self):
		return self.subsession.round_number == 1

	# variables for use in template
	def vars_for_template(self):
		try:
			bomb_row = self.player.bomb_location.split(',')[0]
			bomb_row = bomb_row.replace('{"row":','')
			bomb_col = self.player.bomb_location.split(',')[1]
			bomb_col = bomb_col.replace('"col":','')
			bomb_col = bomb_col.replace('}','')
		except:
			bomb_row = 1
			bomb_col = 1



		return {
			'player_in_all_rounds':   self.player.in_all_rounds(),
			'box_value':              Constants.box_value,
			'boxes_total':            Constants.num_rows * Constants.num_cols,
			'boxes_collected':        self.player.boxes_collected,
			'bomb':                   self.player.bomb,
			'bomb_row':               bomb_row,
			'bomb_col':               bomb_col,
			'round_result':           self.player.round_result,
		}


class WaitFinal(WaitPage):
    title_text = "Attendi"
    body_text = "Attendi per iniziare il prossimo task"
    wait_for_all_groups = True


page_sequence = [
	InstructionsBret,
	Bret,
	ResultsBret
	# WaitFinal
]
