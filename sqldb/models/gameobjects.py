from .basemodels import *

class GameObject(OwnedObject, TableModel):
	filepath = TextField(default="")
	created_date = DateTimeField(default=datetime.datetime.now)
	is_public = BooleanField(default=False)

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
		if self._modelObj:
			self._modelObj.save()
			self.filepath = self._modelObj._storageLocation
		super().save(*p, **pn)

	# Object creation

	def populateFields(self):
		""" Fill the fields values with the values found in the object """
		pass

	@classmethod
	def createFrom(cls, model, **namedParams):
		obj = cls.create(**namedParams)
		obj._modelObj = model
		obj.populateFields()
		obj.save()
		return obj