from ..maintestmodel import MainTestModel
from sqldb.db import *
from sqldb.models import *
from sqldb.models.user import User
import onb

class SqldbTestModel(MainTestModel):
	dataAlreadyGenerated = False
	@classmethod
	def setUpClass(cls):
		if not SqldbTestModel.dataAlreadyGenerated:
			# Ensure tables are created for the first test
			generateStructure()
			cls.generateBaseTestDatas()
			SqldbTestModel.dataAlreadyGenerated = True

	@classmethod
	def clearTables(cls, classname):
		for modelClass in classname.__subclasses__():
			modelClass.delete().execute()
			cls.clearTables(modelClass)
	
	@classmethod
	def generateBaseTestDatas(cls):
		""" Use this when you need a clean database with default values """
		cls.clearTables(basemodels.SqlTableModel)
		generateBaseTestDatas()

	def setUp(self):
		super().setUp()
		if onb.sqldb.is_closed():
			onb.sqldb.connect()
	
	def tearDown(self):
		super().tearDown()
		if not onb.sqldb.is_closed():
			onb.sqldb.close()