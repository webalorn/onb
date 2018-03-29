class FieldValue:
	"""
	Field with a fixed type and a default value
	"""
	def type(self):
		return None

	def createValue(self):
		return self.type()()

	def castFunction(self, value):
		try:
			return self.type()(value)
		except:
			return self.createValue()

	def __init__(self, defaultValue=None):
		self.defaultValue = self.castFunction(defaultValue)

	def __repr__(self):
		return str((self.__class__.__name__, self.get()))

### Base types

class IntField(FieldValue):
	""" Field that only store int values """
	def type(self):
		return int

class BoolField(FieldValue):
	""" Field that only store bool values """
	def type(self):
		return bool

class StringField(FieldValue):
	""" Field that only store string values """
	def type(self):
		return str

class FloatField(FieldValue):
	""" Field that only store float values """
	def type(self):
		return float

### Complex types

class ClassField(FieldValue):
	""" Field that only store instances of the same class """
	def type(self):
		return self.className

	def createValue(self):
		return self.type()(*self.classParams)

	def __init__(self, className, *classParams):
		if isinstance(className, str):
			from ..modelslist import getModelByName
			className = getModelByName(className)

		self.className = className
		self.classParams = classParams
		FieldValue.__init__(self)

### Dictionary

from .dictmodelfield import *

class DictField(ClassField):
	def __init__(self, fieldsSharedType):
		ClassField.__init__(self, DictModel, fieldsSharedType)