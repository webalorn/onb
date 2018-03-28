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
	""" Field that only store an instance of a class """
	def type(self):
		return self.className

	def __init__(self, className):
		self.className = className
		FieldValue.__init__(self)