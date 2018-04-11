from ..sqldbmodel import SqldbTestModel
from sqldb.models.gameobject import *
from engine.engine import Rand
import peewee, os

class GameObjectTest(SqldbTestModel):
	def setUp(self):
		self.modelClass = sqlModels['unit']
		self.sqlModel = self.modelClass.create(model={})

	def test_defaultValues(self):
		self.assertEqual(self.sqlModel.owner, None)
		self.assertEqual(self.sqlModel.is_official, False)
		self.assertEqual(self.sqlModel.is_public, True)
		self.assertEqual(self.sqlModel.is_generated, False)

	def test_modelFields(self):
		exposedFields = self.sqlModel.model.getExposedFields()
		props = {field:Rand.randomString() for field in exposedFields if self.sqlModel.model.getFieldType(field) == str}

		self.sqlModel = self.modelClass.create(model=props)
		for key, val in props.items():
			self.assertEqual(getattr(self.sqlModel, key), val)

	def test_delete(self):
		filepath = onb.getDbPath(self.sqlModel.model._storageLocation)
		model_id = self.sqlModel.id

		self.assertTrue(self.modelClass.select().where(self.modelClass.id == model_id).exists())
		self.assertTrue(os.path.isfile(filepath))

		self.sqlModel.delete_instance()

		self.assertFalse(self.modelClass.select().where(self.modelClass.id == model_id).exists())
		self.assertFalse(os.path.isfile(filepath))