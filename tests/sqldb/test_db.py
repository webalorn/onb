from .sqldbmodel import SqldbTestModel
from sqldb.db import tables
import onb

class dbTest(SqldbTestModel):
	def test_tablesExist(self):
		self.assertNotEqual(len(tables), 0)
		self.assertNotEqual(len(onb.sqldb.get_tables()), 0)