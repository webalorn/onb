from .gameentities import BaseGameModel, GameEntityModel
from ..datas.fieldvalues import *

class CreatureModel(GameEntityModel):
	def getFields():
		return {
			'initiative': IntField(min=0),
			'actions': ClassField('actions'),
			'abilities': ClassField('abilities'),
		}
	storable = True

class ObjectModel(GameEntityModel):
	def getFields():
		return {
			'alignment': StringField(values=["unaligned"]),
			'race': StringField(values=["object"]),
		}

### Characteristics

class AbilitiesModel(BaseGameModel):
	def getFields():
		return {
			'parry': IntField(),
			'dodge': IntField(),
			'dodge_ranged_attack': IntField(),
			'mental_attack_defence': IntField(),

			'strength': IntField(),
			'dexterity': IntField(),
			'agility': IntField(),
		}

class ProtectionModel(BaseGameModel):
	def getFields():
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

class ActionsModel(BaseGameModel):
	def getFields():
		return {
			'attacks': DictField(ClassField('attack')),
			'moves': DictField(ClassField('actions_moves')),
		}


class AttackModel(BaseGameModel):
	def getFields():
		return {
			'weapon_name': StringField(),
			'dammages_type': StringField(),
			'parry_hardness': IntField(),
			'dodge_hardness': IntField(),
			'attack_strength': IntField(),
			'parry_required_strength': IntField(),
		}

class ActionsMovesModel(BaseGameModel):
	def getFields():
		return {
			'run_speed' : IntField(1),
			'sprint_speed' : IntField(),
		}