from ..datas.datamodel import DataModel
from ..datas.fieldvalues import *

"""
Allowed Fields:
	-> BoolField (optional default value)
	-> IntField (optional default value)
	-> StringField (optional default value)
	-> FloatField (optional default value)

	-> ClassField (required model type) # The subclasses of the model are allowed
	-> DictField (required fields values type)
"""

class CreatureModel(DataModel):
	def getFields(self):
		return {
			'name': StringField(),

			'initiative': IntField(),
			'health': IntField(1),
			'size': IntField(1),

			'protection': ClassField('protection'),
			'actions': ClassField('actions'),
			'abilities': ClassField('abilities'),
		}

### Characteristics

class AbilitiesModel(DataModel):
	def getFields(self):
		return {
			'parry': IntField(),
			'dodge': IntField(),
			'dodge_ranged_attack': IntField(),
			'mental_attack_defence': IntField(),

			'strength': IntField(),
			'dexterity': IntField(),
			'agility': IntField(),
		}

class ProtectionModel(DataModel):
	def getFields(self):
		return {
			'armor_cutting': IntField(),
			'armor_blunt': IntField(),
			'armor_piercing': IntField(),

			'fire_bonus': IntField(),
			'ice_bonus': IntField(),
			'electricity_bonus': IntField(),
			'acid_bonus': IntField(),
		}

### Actions

def getDiceField():
	return IntField()

def diceDammagesFields():
	return {
		'dice': getDiceField(),
		'bonus': IntField(),
	}

def diceRollFields():
	return {
		'dice': getDiceField(),
		'difficulty': IntField(),
	}

class ActionsModel(DataModel):
	def getFields(seld):
		return {
			'attacks': DictField(ClassField('attack')),
			'moves': DictField(ClassField('actions_moves')),
		}


class AttackModel(DataModel):
	def getFields(self):
		return {
			'weapon_name': StringField(),
			'dammages_type': StringField(),
			'parry_hardness': IntField(),
			'dodge_hardness': IntField(),
			'attack_strength': IntField(),
			'parry_required_strength': IntField(),

			**diceDammagesFields(),
		}

class ActionsMovesModel(DataModel):
	def getFields(self):
		return {
			'run_speed' : IntField(1),
			'sprint_speed' : IntField(),
		}