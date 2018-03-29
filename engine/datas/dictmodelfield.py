from .datamodel import *
from .fieldvalues import FieldValue

class DictModel(DataModel):
	""" A dictionary that can store a variable number of datas """

	def fieldExist(self, key):
		return True

	def getConvertedFieldValue(self, fieldName, newValue):
		return self.fieldsSharedType.castFunction(newValue)

	def __init__(self, fieldsSharedType):
		""" all objects must inherit from the same class """
		self.fieldsSharedType = fieldsSharedType
		DataModel.__init__(self)

		if not isinstance(self.fieldsSharedType, FieldValue):
			raise TypeError("DictModel type must be a subclass of FieldValue")

	def ensureFieldExists(self, fieldName):
		if not fieldName in self.fields:
			self.fields[fieldName] = self.getConvertedFieldValue(fieldName, None)