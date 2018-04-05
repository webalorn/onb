from .basemodels import *
from engine.modelslist import getModelByName
from .customfields import ModelField
from engine.models import *

sqlModels = []

def _addSubModelsToSqlModel(classname):
	for modelClass in classname.__subclasses__():
		if modelClass.storable:
			sqlModels.append(modelClass.getModelName())
		_addSubModelsToSqlModel(modelClass)
_addSubModelsToSqlModel(gameentities.BaseGameModel)

class GameObject(OwnedObject):

	created_date = DateTimeField(default=datetime.datetime.now)
	updated_date = DateTimeField(default=datetime.datetime.now)

	modelClass = 'game_entity'
	model = ModelField(modelClass, unique=True)
	type = TextField(default=modelClass)

	def populateFields(self):
		""" Fill the fields values with the values found in the object """
		if not self.model:
			raise TypeError("Model value can't be empty")

		for key in self.model.getExposedFields():
			setattr(self, key, self.model[key])

		self.type = self.model.getModelName()
		self.updated_date = datetime.datetime.now()

	def save(self, *p, **pn):
		self.populateFields()
		super().save(*p, **pn)

	@staticmethod
	def createGameObjectModel(modelName):
		sqlTableName = (modelName + '_table').title()
		classModel = getModelByName(modelName)
		properties = {
			'modelClass': modelName,
			'model': ModelField(modelName, unique=True),
			'type': TextField(default=modelName),
		}

		fieldTypes = {
			'string': TextField,
			'int': IntegerField,
			'float': FloatField,
			'bool': BooleanField,
		}

		for key in classModel.getExposedFields():
			fieldType = fieldTypes[classModel.getFieldTypes()[key].getTypeRep()]
			properties[key] = fieldType(null=True)

		return type(sqlTableName, (GameObject, TableModel,), properties)

sqlModels = { key : GameObject.createGameObjectModel(key) for key in sqlModels }