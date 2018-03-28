from .dataModel import DataModel
from .fieldvalues import *

class DataCreature(DataModel):
	def getFields(self):
		return {
			'health': IntField(31),
			'name': StringField("foo"),
			'floatValue': FloatField(4.2),
			'array': ClassField(list),
		}