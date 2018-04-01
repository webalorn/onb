from .datamodel import *
from .fieldvalues import FieldValue

class DictModel(DataModel):
	""" A dictionary that can store a variable number of datas """

	def fieldExist(self, key):
		return True

	def getFieldObj(self, fieldName):
		return self.fieldsSharedType

	def getConvertedFieldValue(self, fieldName, newValue):
		self.ensureFieldExists(fieldName)
		return self.fieldsSharedType.castFunction(newValue)

	def __init__(self, fieldsSharedType):
		""" all objects must inherit from the same class """
		self.fieldsSharedType = fieldsSharedType
		DataModel.__init__(self)

		if not isinstance(self.fieldsSharedType, FieldValue):
			raise TypeError("DictModel type must be a subclass of FieldValue")

	def createNewInstance(self):
		return type(self)(self.fieldsSharedType)

	def ensureFieldExists(self, fieldName):
		if not fieldName in self.fields:
			self.fields[fieldName] = self.fieldsSharedType.defaultValue()

	def setValues(self, valuesList):
		self.fields = {}
		for key in valuesList:
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