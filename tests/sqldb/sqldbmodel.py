from ..maintestmodel import MainTestModel
from sqldb.db import generateStructure
import onb

class SqldbTestModel(MainTestModel):
	@classmethod
	def setUpClass(cls):
		generateStructure()
	
	def setUp(self):
		onb.sqldb.connect()
	
	def tearDown(self):
		if not onb.sqldb.is_closed():
			onb.sqldb.close()