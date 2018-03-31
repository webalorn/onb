from ..datas.datamodel import DataModel
from ..datas.fieldvalues import *

class DammageTableModel(DataModel):
	def getFields(self):
		return {
			'baseValue': IntField(12),
			'values': ListField(IntField(12))
		}

class TableFamilyModel(DataModel):
	def getFields(self):
		return {
			'tables': ClassField('dammage_table'),
			'generator': StringField(),
		}