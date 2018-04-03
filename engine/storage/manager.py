import onb, os
from engine.engine import Singleton
import engine.storage.jsondb as jsondb

class StorageManager(metaclass=Singleton):
	"""
	Manage storage of the models in the db folder, only load each model once
	
	All path must be relative to the db location definaed in onb
	"""
	def __init__(self):
		self.files = {}

	### Internal

	def _createModelFile(self, model):
		path = onb.getDbPath('{0}.json'.format(model.getModelName()), newFile=True)
		relPath = os.path.relpath(path, onb.conf.dbFilesLocation)
		model._storageLocation = relPath
		self._storeModel(model)

	def _getRealPath(self, path):
		return onb.getDbPath(path)

	def _storeModel(self, model):
		if onb.conf.cacheAllModels:
			self.files[model._storageLocation] = model

	### External functions
	def clearCache(self):
		self.files = {}

	def load(self, path):
		if not path in self.files:
			model = jsondb.readModelFrom(self._getRealPath(path))
			model._storageLocation = path
			self._storeModel(model)
			return model
		else:
			return self.files[path]

	def save(self, model):
		if not model._storageLocation:
			self._createModelFile(model)
		path = model._storageLocation
		jsondb.storeTo(model, self._getRealPath(path))
		return path