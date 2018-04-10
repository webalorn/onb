from .gamemodels import *

### Characteristics

class AttributesModel(BaseGameModel):
	def getFields():
		return {
			'strength': IntField(),
			'dexterity': IntField(),
			'agility': IntField(),
		}

class SkillsModel(BaseGameModel):
	def getFields():
		return {
			'parry': IntField(),
			'dodge': IntField(),

			'parry_accuracy': PercentField(),
			'dodge_accuracy': PercentField(),
		}

class PassiveModel(BaseGameModel):
	def getFields():
		return {
			
		}

### Actions

class ActionModel(BaseGameModel):
	def getFields():
		return {}


class AttackModel(ActionModel):
	def getFields():
		return {
			'attack_type': StringField(values=['contact']),
			'dammages_type': StringField(values=gameConf.dammageTypes),
			'power_type': StringField(values=gameConf.powerTypes, default='material'),
			'range': IntField(1),

			'dammages': IntField(),
			'attack_bonus': IntField(),
			'mastery_coeff': PercentField(),
			'dodge_hardness': PercentField(),

			'base_accuracy': PercentField(),
			'mastery_accuracy': PercentField(),
		}

class ContactAttack(AttackModel):
	def getFields():
		return {
			'attack_strength_bonus': IntField(),
		}

class RangedAttackModel(AttackModel):
	def getFields():
		return {
			'projectile_strenght': IntField(),
			'coeff_bonus_unit_strenght': IntField(),
		}

class ActionMoveModel(ActionModel):
	def getFields():
		return {
			'run_speed' : IntField(1),
			'sprint_speed' : IntField(),
		}