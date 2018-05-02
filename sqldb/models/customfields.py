from .basemodels import *
from engine.modelslist import getModelByName
from engine.storage.encoder import *
import json
from peewee import *

class ModelField(TextField):
	def __init__(self, modelType, *p, **pn):
		super().__init__(*p, **pn)
		if isinstance(modelType, str):
			modelType = getModelByName(modelType)
		self._modelType = modelType

	def db_value(self, model):
		if isinstance(model, dict):
			model = self._modelType(model)
		if isinstance(model, self._modelType):
			return json.dumps(ModelEncoder().encode(model))
		else:
			raise TypeError("Model is not an instance of {0}".format(self._modelType.getModelName()))

	def python_value(self, value):
		return ModelEncoder().decode(json.loads(value))

class PyDataField(TextField):
	def db_value(self, value):
		return json.dumps(value)

	def python_value(self, value):
		return json.loads(value)