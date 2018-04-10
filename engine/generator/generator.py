from ..datas.datamodel import DataModel
from ..storage.manager import StorageManager

class ModelGenerator():
	modelClass = DataModel

	@classmethod
	def generate(cls, model):
		"""
		Generate datas in the model
		"""
		if isinstance(model, cls.modelClass):
			return model
		else:
			raise TypeError("Model is not an instance of {0}".format(A.__name__))

	@classmethod
	def generateFromFile(cls, filename, autoSave=True):
		model = StorageManager().load(filename)
		model = cls.generate(model)
		if autoSave:
			model.save()
		return model

	@classmethod
	def new(cls):
		model = cls.modelClass()
		cls.generate(model)
		return model