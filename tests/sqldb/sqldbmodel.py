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
		cls.clearTables(basemodels.TableModel)
		unitModel = gameobject.sqlModels['unit']
		user = User.create(username="test_user", password_hash=User.hashPassword('1234'))
		for k in range(5):
			unitModel.create(model={'name':'unit'+str(k+1), 'health':k}, owner_id=user.id)

		if not onb.sqldb.is_closed():
			onb.sqldb.close()

	def setUp(self):
		super().setUp()
		if onb.sqldb.is_closed():
			onb.sqldb.connect()
	
	def tearDown(self):
		super().tearDown()
		if not onb.sqldb.is_closed():
			onb.sqldb.close()