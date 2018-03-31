class FieldValue:
	"""
	Field with a fixed type and a default value
	"""
	def type(self):
		return None

	def createValue(self):
		return self.type()()

	def castFunction(self, value):
		if value == None:
			value = self.createValue()
		else:
			try:
				value = self.type()(value)
			except:
				value = self.createValue()

		value = self.setUnderMax(value)
		value = self.setAboveMin(value)
		value = self.setInValidValues(value)

		return value

	def setUnderMax(self, value):
		if self.maxi != None and value > self.maxi:
			return self.type()(self.maxi)
		return value

	def setAboveMin(self, value):
		if self.mini != None and value < self.mini:
			return self.type()(self.mini)
		return value

	def setInValidValues(self, value):
		if isinstance(self.values, list) and self.values and not value in self.values:
			if hasattr(self, 'defaultValue'):
				return self.defaultValue
			return self.values[0]
		return value

	def __init__(self, default=None, *parameters, values=None, mini=None, maxi=None):
		"""
			Values defines the different possible values
			Mini defines the minimum value/size
			Maxi defines the maximum value/size
		"""
		self.values = values
		self.mini = mini
		self.maxi = maxi
		self.defaultValue = self.castFunction(default)

	def __repr__(self):
		return str((self.__class__.__name__, self.get()))

### Base types

class BoolField(FieldValue):
	""" Field that only store bool values """
	def type(self):
		return bool

class IntField(FieldValue):
	""" Field that only store int values """
	def type(self):
		return int

class FloatField(FieldValue):
	""" Field that only store float values """
	def type(self):
		return float

class StringField(FieldValue):
	""" Field that only store string values """
	def type(self):
		return str

	def setUnderMax(self, value):
		if self.maxi != None and len(value) > self.maxi:
			return value[:self.maxi]
		return value

	def setAboveMin(self, value):
		if self.mini != None and len(value) < self.mini:
			value += "#"*(self.mini-len(value))
		return value

### Complex types

class ClassField(FieldValue):
	""" Field that only store instances of the same class """
	def type(self):
		return self.className

	def createValue(self):
		return self.type()(*self.classParams)

	def castFunction(self, value):
		try:
			return self.type()(value)
		except:
			return self.createValue()

	def __init__(self, className, *classParams):
		if isinstance(className, str):
			from ..modelslist import getModelByName
			className = getModelByName(className)

		self.className = className
		self.classParams = classParams
		FieldValue.__init__(self)

### Structures

from .structfields import *

class DictField(ClassField):
	def __init__(self, fieldsSharedType):
		ClassField.__init__(self, DictModel, fieldsSharedType)

class ListField(ClassField):
	def __init__(self, fieldsSharedType):
		ClassField.__init__(self, ListModel, fieldsSharedType)