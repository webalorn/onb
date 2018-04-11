from .basemodels import *
from engine.modelslist import getModelByName
from engine.storage.manager import StorageManager
from .customfields import ModelField
from engine.models import *

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

	def delete_instance(self, *p, **pn):
		StorageManager().delete(self.model)
		self.model = None
		super().delete_instance()

	@staticmethod
	def _createGameObjectModel(modelName):
		""" Create a new class to save a specific model"""
		sqlTableName = (modelName + '_table').title()
		classModel = getModelByName(modelName)
		properties = {
			'modelClass': modelName,
			'model': ModelField(modelName, unique=True),
			'type': TextField(default=modelName),
		}

		for key in classModel.getExposedFields():
			fieldType = _fieldTypes[classModel.getFieldTypes()[key].getTypeRep()]
			properties[key] = fieldType(null=True)

		return type(sqlTableName, (GameObject, TableModel,), properties)

sqlModels = { key : GameObject._createGameObjectModel(key) for key in sqlModels }