from .dataModel import DataModel
from .fieldvalues import *

class DataCreature(DataModel):
	def getFields(self):
		return {
			'health': IntField(31),
			'name': StringField("foo"),
			'floatValue': FloatField(4.2),
			'armor': ClassField(DataArmor),
		}

class DataArmor(DataModel):
	def getFields(self):
		return {
			'protection': IntField(10),
		}