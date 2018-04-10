"""
Base class for all entities (creatures, objects)
"""

from .gamemodels import *
from .unitstats import *
from .equipments import *

class GameEntityModel(BaseGameModel):
	def getFields():
		print("GET fields")
		return {
			'name': StringField(),
			'alignment': StringField(default="neutral", helperList="alignment"),
			'race': StringField(helperList="race"),
			'subrace': StringField(helperList="subraces"),
			'universe': StringField(helperList="universes"),
			'battleground': StringField(helperList="battlegrounds"),

			'life_points': IntField(1),
			'health': IntField(1),
			'size': IntField(3),
			'base_size': IntField(3),
			'mana': IntField(),

			'armor': ClassField('armor'),

			# Generated values
			'categories': ListField(StringField(), generated=True),
		}
	exposedFields = ['name', 'race', 'sub_race', 'alignment', 'universe', 'battleground']

class ObjectModel(DbStorableModel, GameEntityModel):
	def getFields():
		return {
			# rewrite fields
			'alignment': StringField(values=["unaligned"]),
			'race': StringField(values=["object"]),
		}

class UnitModel(DbStorableModel, GameEntityModel):
	"""
	Any entity that can move and, eventualy, be added in an army
	"""

	def getFields():
		return {
			'cost': IntField(),
			'initiative': IntField(min=0),
			'unit_type': StringField("troop", "hero", "npc"),

			'movement': ClassField('action_move'),
			'attributes': ClassField('attributes'),
			'skills': ClassField('skills'),

			'weapons': ListField('weapon'),
			'actions': ListField('action'),
			'passives': ListField('passive'),
		}

	def getActions():
		return [
			*self.actions.getList(),
			*[weapon.getActions() for weapon in self.weapons.getList()],
			self.movement
		]
