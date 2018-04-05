from .basemodels import *
from engine.modelslist import getModelByName
from engine.storage.manager import StorageManager

class ModelField(TextField):
	def __init__(self, modelType, *p, **pn):
		super().__init__(*p, **pn)
		if isinstance(modelType, str):
			modelType = getModelByName(modelType)
		self._modelType = modelType

	def db_value(self, model):
		if isinstance(model, self._modelType):
			model.save()
			return model._storageLocation
		else:
			raise TypeError("Model is not an instance of {0}".format(self._modelType.getModelName()))

	def python_value(self, value):
		return StorageManager().load(value)