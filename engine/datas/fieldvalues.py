import copy

class FieldValue:
	"""
	Field with a fixed type and a default value
	"""

	values = []
	generated = False
	min, max, helperList, default = None, None, None, None

	def type(self):
		return None

	@classmethod
	def getTypeRep(cls):
		return cls.__name__[:-5].lower()

	def createValue(self):
		return self.type()()

	def createValueFrom(self, otherValue):
		return None

	def castFunction(self, value):
		value = copy.deepcopy(value) # ensure it will create a new object
		if value == None:
			value = self.createValue()
		elif not isinstance(value, self.type()):
			cleverCast = self.createValueFrom(value)
			if cleverCast != None:
				value = cleverCast
			else: # Hard cast
				try:
					value = self.type()(value)
				except:
					value = self.createValue()

		value = self.setUnderMax(value)
		value = self.setAboveMin(value)
		value = self.setInValidValues(value)

		return value

	def getDbValue(self, value):
		return value

	def defaultValue(self):
		return self.castFunction(self.default)

	def setUnderMax(self, value):
		if self.max != None and value > self.max:
			return self.type()(self.max)
		return value

	def setAboveMin(self, value):
		if self.min != None and value < self.min:
			return self.type()(self.min)
		return value

	def setInValidValues(self, value):
		if isinstance(self.values, list) and self.values and not value in self.values:
			return self.values[0]
		return value

	def __init__(self, default=None, *parameters, **namedParams):
		"""
			Values defines the different possible values
			min defines the minmum value/size
			max defines the maxmum value/size
		"""
		self.default = default
		for attr in namedParams:
			if hasattr(self, attr):
				setattr(self, attr, namedParams[attr])
		

	def __repr__(self):
		return str((self.__class__.__name__,))

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
		if self.max != None and len(value) > self.max:
			return value[:self.max]
		return value

	def setAboveMin(self, value):
		if self.min != None and len(value) < self.min:
			value += "#"*(self.min-len(value))
		return value

### Complex types

class ClassField(FieldValue):
	""" Field that only store instances of the same class """
	def type(self):
		return self.className

	def createValue(self):
		return self.type()(*self.classParams)

	def __init__(self, className, classParams=[], *p, **pn):
		if isinstance(className, str):
			from ..modelslist import getModelByName
			className = getModelByName(className)

		self.className = className
		self.classParams = classParams
		FieldValue.__init__(self, *p, **pn)

class ForeignKeyField(FieldValue):
	""" Field that only store instances of the same class """

	def type(self):
		from ..modelslist import getModelByName
		return getModelByName(self.modelName)

	def defaultValue(self):
		return self.castFunction(self.default)
	
	def createValue(self):
		return None

	def getDbValue(self, value):
		if hasattr(value, '_foreignKeyId'):
			return value._foreignKeyId

	def createValueFrom(self, key):
		from ..modelslist import getModelByName
		from sqldb.models.gameobject import sqlModels
		
		try:
			key = int(key)
			model = sqlModels[self.modelName].get(id=key).model
			model._foreignKeyId = key
			return model
		except: # cast error -> invalid data or None value
			pass

		if isinstance(key, str): # if the model is created with a string, it will create an empty model that won't be saved
			key = getModelByName(key)()
		if isinstance(key, getModelByName(self.modelName)):
			return key
		return None

	def __init__(self, modelName, *p, **pn):
		self.modelName = modelName
		super().__init__(*p, **pn)

### Structures

from .structfields import *

class DictField(ClassField):
	def __init__(self, fieldsSharedType, *p, **pn):
		ClassField.__init__(self, DictModel, [fieldsSharedType], *p, **pn)

	def createValueFrom(self, otherValue):
		if isinstance(otherValue, dict):
			cleverCast = self.createValue()
			cleverCast.setValues(otherValue)
			return cleverCast

class ListField(ClassField):
	def __init__(self, fieldsSharedType, *p, **pn):
		ClassField.__init__(self, ListModel, [fieldsSharedType], *p, **pn)

	def createValueFrom(self, otherValue):
		if isinstance(otherValue, list):
			cleverCast = self.createValue()
			cleverCast.setValues(otherValue)
			return cleverCast