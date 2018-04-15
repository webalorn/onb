from .gameentities import BaseGameModel
from ..datas.fieldvalues import *

class GameTableModel(BaseGameModel):
	def getFields():
		return {
			'first_line': IntField(),
			'last_line': IntField(),
			'pv_advance': ListField(IntField(1)),
			'by_lines_interval': ListField(IntField(1)), # dammages increase by 'pv_advance' each 'by_id_interval' points

			'table': ListField(ListField(IntField()), generated=True)
		}