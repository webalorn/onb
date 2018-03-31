import onb, os
from engine.engine import Singleton
import engine.storage.jsondb as jsondb

class StorageManager(metaclass=Singleton):
	""" All path must be relative to the db location definaed in onb """
	def __init__(self):
		self.files = {}

	### Internal

	def _createModelFile(self, model):
		path = onb.getDbPath('{0}.json'.format(model.getModelName()), newFile=True)
		relPath = os.path.relpath(path, onb.conf.dbLocation)

		model._storageLocation = relPath
		self.files[relPath] = model

	def _getRealPath(self, path):
		return onb.getDbPath(path)

	### External functions
	def load(self, path):
		if not path in self.files:
			self.files[path] = jsondb.readModelFrom(self._getRealPath(path))
			self.files[path]._storageLocation = path
		return self.files[path]

	def save(self, model):
		if isinstance(model, str):
			path = model
			jsondb.storeTo(self.files[path], self._getRealPath(path))
			return path
		else:
			if not model._storageLocation:
				self._createModelFile(model)
			return self.save(model._storageLocation)