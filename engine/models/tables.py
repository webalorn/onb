from ..datas.datamodel import DataModel
from ..datas.fieldvalues import *

class DammageTableModel(DataModel):
	def getFields(self):
		return {
			'base_value': IntField(12),
			'values': ListField(IntField(12))
		}

class TableFamilyModel(DataModel):
	def getFields(self):
		return {
			'generator': StringField(),
			'first_base_value': IntField(),
			'last_base_value': IntField(),
			'nb_values': IntField(min=0),

			'tables': ClassField('dammage_table'),
		}