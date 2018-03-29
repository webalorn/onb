from ..datas.datamodel import DataModel
from ..datas.fieldvalues import *

class CreatureModel(DataModel):
	def getFields(self):
		return {
			'health': IntField(31),
			'name': StringField("foo"),
			'floatValue': FloatField(4.2),
			'armor': ClassField('armor'),
			'actions': DictField(IntField(42)),
		}

class ArmorModel(DataModel):
	def getFields(self):
		return {
			'protection': IntField(10),
		}