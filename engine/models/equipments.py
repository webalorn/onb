from .gamemodels import *
from .unitstats import *

### Protection and armor

class ArmorModel(BaseGameModel):
	def getFields():
		return {
			'armor': IntField(),
			'bonuses': DictField(IntField(), keysIn=gameConf.dammageTypes + gameConf.powerTypes),
		}

### Weapons

class Weapon(DescribedModel):
	def getFields():
		return {
			'actions': ListField('action'), # Attack(s) and, eventually, other possible actions

			# Parry attack with this weapon
			'parry_bonus': IntField(),
			'parry_contact_coeff': PercentField(),
			'parry_ranged_coeff': PercentField(default=0),
			'parry_strength_bonus': IntField(),
		}

	def getActions():
		return self.actions.getList()