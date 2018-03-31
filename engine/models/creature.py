from .gameentities import GameEntityModel
from ..datas.fieldvalues import *



class CreatureModel(GameEntityModel):
	def getFields(self):
		return {
			**super().getFields(),

			'initiative': IntField(),
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
		}

class ActionsMovesModel(DataModel):
	def getFields(self):
		return {
			'run_speed' : IntField(1),
			'sprint_speed' : IntField(),
		}