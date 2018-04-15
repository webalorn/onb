from .basemodels import *
from .user import OwnedObject
from engine.modelslist import getModelByName
from engine.storage.manager import StorageManager
from engine.engine import notAlphaNumRegex
from .customfields import ModelField
from engine.models import *
from playhouse.sqlite_ext import *

sqlModels = []

_fieldTypes = {
	'string': TextField,
	'int': IntegerField,
	'float': FloatField,
	'bool': BooleanField,
}

def _addSubModelsToSqlModel(classname):
	for modelClass in classname.__subclasses__():
		if modelClass.storable:
			sqlModels.append(modelClass.getModelName())
		_addSubModelsToSqlModel(modelClass)
_addSubModelsToSqlModel(gameentities.BaseGameModel)

sqlModelsIndexes = {}
print("->", FTS5Model.fts5_installed())
class GameObjectIndex(FTSModel):
	rowid = RowIDField()

	class Meta:
		database = onb.sqldb
		options = {'tokenize': 'porter'}

	def _createGameObjectIndex(modelName, fields):
		properties = {name:SearchField() for name in fields}
		sqlTableName = (modelName + '_index_table').title()
		sqlModelsIndexes[modelName] = type(sqlTableName, (GameObjectIndex, SqlTableModel,), properties)
		return sqlModelsIndexes[modelName]


class GameObject(OwnedObject):
	modelClass = 'game_entity'
	model = ModelField(modelClass, unique=True)
	type = TextField(default=modelClass)

	def populateFields(self):
		""" Fill the fields values with the values found in the object """
		if isinstance(self.model, dict):
			self.model = getModelByName(self.modelClass)(self.model)
		if not self.model:
			raise TypeError("Model value can't be empty")

		for key in self.model.getExposedFields():
			setattr(self, key, self.model[key])

		self.type = self.model.getModelName()

	def save(self, *p, **pn):
		self.populateFields()
		super().save(*p, **pn)

		indexRow, created = self.searchTable.get_or_create(rowid=self.id)
		for fieldName in self.exposedFields:
			setattr(indexRow, fieldName, getattr(self, fieldName))
		indexRow.save()

	def delete_instance(self, *p, **pn):
		StorageManager().delete(self.model)
		self.model = None
		super().delete_instance()

	@classmethod
	def search(cls, phrase):
		""" Search phrase will be converted to lowercase letters and nums prefixs"""
		phrase = notAlphaNumRegex.sub('', phrase).lower().split()
		phrase = [word + '*' for word in phrase]
		phrase = " OR ".join(phrase)

		return (cls.select().join(
				cls.searchTable,
				on=(cls.id == cls.searchTable.rowid))
			.where(cls.searchTable.match(phrase))
			.order_by(cls.searchTable.bm25()))

	@staticmethod
	def _createGameObjectModel(modelName):
		""" Create a new class to save a specific model"""
		sqlTableName = (modelName + '_table').title()
		classModel = getModelByName(modelName)
		exposedFields = classModel.getExposedFields()
		properties = {
			'exposedFields': exposedFields,
			'searchTable': GameObjectIndex._createGameObjectIndex(modelName, exposedFields),
			'modelClass': modelName,
			'model': ModelField(modelName, unique=True),
			'type': TextField(default=modelName),
		}

		for key in exposedFields:
			fieldType = _fieldTypes[classModel.getFieldTypes()[key].getTypeRep()]
			properties[key] = fieldType(null=True)

		return type(sqlTableName, (GameObject, SqlTableModel,), properties)

sqlModels = { key : GameObject._createGameObjectModel(key) for key in sqlModels }