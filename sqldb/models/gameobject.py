from .basemodels import *
from engine.modelslist import getModelByName

class GameObject(OwnedObject):
	modelClass = 'game_entity'

	filepath = TextField(unique=True)
	created_date = DateTimeField(default=datetime.datetime.now)

	type = TextField(default=modelClass)

	def populateFields(self, model):
		""" Fill the fields values with the values found in the object """
		self.filepath = model._storageLocation
		self.name = model.name
		self.type = model.getModelName()

	# Get and save linked object
	_modelObj = None

	def getModel(self):
		from engine.storage.manager import StorageManager
		if not self._modelObj:
			try:
				self._modelObj = StorageManager().load(self.filepath)
			except:
				pass
		return self._modelObj

	def save(self, *p, **pn):
		if self._modelObj: # If the object is not loaded, it hasn't changed
			self._modelObj.save()
			self.populateFields(self._modelObj)
		super().save(*p, **pn)

	# Object creation

	@classmethod
	def createFrom(cls, model, **namedParams):
		clsClass = getModelByName(cls.modelClass)
		if isinstance(model, clsClass):
			obj = cls(**namedParams)
			obj._modelObj = model
			obj.save(force_insert=True)
			return obj
		else:
			raise TypeError("{0} is not an instance of {1}".format(model.getModelName(), clsClass.getModelName()))