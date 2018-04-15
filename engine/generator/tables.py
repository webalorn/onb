from .generator import ModelGenerator
from ..models.tables import GameTableModel
import onb

class TableGenerator(ModelGenerator):
	modelClass = GameTableModel

	defaultFirstLine = onb.conf.game.diceSuccess
	defaultLastLine = defaultFirstLine + 19
	defaultColumns = [(1, 20), (1, 10), (1, 8), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1)]

	@classmethod
	def generateColumn(cls, size, pvAdvance, byLinesInterval):
		return [1 + (pvAdvance * line) // byLinesInterval for line in range(0, size)]
	
	@classmethod
	def generate(cls, *p, **pn):
		model = super().generate(*p, **pn)
		model.first_line = cls.defaultFirstLine
		model.last_line = cls.defaultLastLine
		for pvAdvance in cls.defaultColumns:
			model.pv_advance.append(pvAdvance[0])
			model.by_lines_interval.append(pvAdvance[1])

		for col in range(model.pv_advance.getMaxKey()+1):
			model.table[col] = cls.generateColumn(model.last_line - model.first_line + 1,
				model.pv_advance[col],
				model.by_lines_interval[col]
			)