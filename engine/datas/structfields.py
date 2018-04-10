from .datamodel import *
from .fieldvalues import FieldValue, ClassField

class DictModel(DataModel):
	""" A dictionary that can store a variable number of datas """

	def fieldExist(self, key):
		return True

	def getFieldObj(self, fieldName):
		return self.fieldsSharedType

	def getConvertedFieldValue(self, fieldName, newValue):
		self.ensureFieldExists(fieldName)
		return self.fieldsSharedType.castFunction(newValue)

	def __init__(self, fieldsSharedType, keysIn=None):
		""" all objects must inherit from the same class """
		self._keysIn = keysIn

		if isinstance(fieldsSharedType, str):
			fieldsSharedType = ClassField(fieldsSharedType)

		self.fieldsSharedType = fieldsSharedType
		DataModel.__init__(self)

		if not isinstance(self.fieldsSharedType, FieldValue):
			raise TypeError("DictModel type must be a subclass of FieldValue")

	def createNewInstance(self):
		return type(self)(self.fieldsSharedType)

	def ensureFieldExists(self, fieldName):
		if not fieldName in self.fields:
			if self._keysIn and not fieldName in self._keysIn:
				raise KeyError("{0} is not in not an allowed key for this Dict".format(fieldName))
			self.fields[fieldName] = self.fieldsSharedType.defaultValue()

	def setValues(self, valuesList):
		self.fields = {}
		for key in valuesList:
			ensureFieldExists(key)
			self[key] = valuesList[key]

class ListModel(DictModel):
	""" A dictionary that can store a variable number of datas with integer keys """

	def assertIsIntKey(self, key):
		try:
			key = int(key)
		except:
			raise KeyError("ListModel keys must be integers")

	def ensureFieldExists(self, fieldName):
		self.assertIsIntKey(fieldName)
		return DictModel.ensureFieldExists(self, fieldName)

	def setKeysRange(self, generator, default = None):
		newFields = {key:self[key] if key in self else None for key in generator}
		self.fields = {}
		for key in newFields:
			self[key] = newFields[key]

	def setValues(self, valuesList):
		self.fields = {}
		for i in range(len(valuesList)):
			self[i] = valuesList[i]

	def getSortedKeys(self):
		return [str(i) for i in sorted([int(i) for i in self.fields.keys()])]

	def getList(self):
		keys = self.getSortedKeys()
		return [self.fields[fieldName] for fieldName in keys]

	def filter(self, fctOrClassname): # Filer by class name
		if isinstance(fctOrClassname, str):
			from ..modelslist import getModelByName
			classModel = getModelByName(fctOrClassname)
			fctOrClassname = lambda obj: isinstance(obj, classModel)

		return list(filter(fctOrClassname, self.getList()))

	def getMaxKey(self):
		if not self.fields:
			return -1
		return max([int(key) for key in self.fields])

	def append(self, value):
		self[self.getMaxKey()+1] = value