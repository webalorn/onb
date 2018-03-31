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

class GameEntityModel(DataModel):
	def getFields(self):
		return {
			'name': StringField(),
			'health': IntField(1),
			'size': IntField(1),
			'protection': ClassField('protection'),
		}