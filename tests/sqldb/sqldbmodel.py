from ..maintestmodel import MainTestModel
from sqldb.db import generateStructure

class SqldbTestModel(MainTestModel):
	@classmethod
	def setUpClass(cls):
		generateStructure()