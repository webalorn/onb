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

class BaseGameModel(DataModel):
	storable = False # Will this model  be directly stored in the database ?
	exposedFields = [] # Field added in the databse entry

class GameEntityModel(BaseGameModel):
	def getFields(self):
		return {
			'name': StringField(),
			'alignment': StringField(default="neutral", helperList="alignment"),
			'race': StringField(helperList="race"),

			'health': IntField(1),
			'size': IntField(1),
			'protection': ClassField('protection'),
		}
	exposedFields = ['name', 'race', 'alignment']