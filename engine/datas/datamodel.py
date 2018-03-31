import re
import copy

class DataModel:
	"""
	Base class for data storgae

	raise: KeyError

	type field name is reserved for the type of the model
	"""


	def getFields(self):
		""" Return a dictionary of all fields. Fields must inherit FieldValue """
		return {}

	def __init__(self):
		""" Must define all values """
		self.fields = {}
		self.fieldTypes = self.getFields()
		for fieldName in self.fieldTypes:
			self.fields[fieldName] = self.fieldTypes[fieldName].defaultValue

	def __repr__(self):
		return str(self.fields)

	### Get Fields and FieldClass 

	def fieldsList(self):
		return self.fields.keys()

	def fieldExist(self, fieldName):
		return fieldName in self.fieldTypes

	def ensureFieldExists(self, fieldName):
		if not fieldName in self.fields:
			raise KeyError("Field {0} doesn't exist".format(fieldName))

	def getFieldObj(self, fieldName):
		if not fieldName in self.fieldTypes:
			raise KeyError()
		return self.fieldTypes[fieldName]

	def getFieldType(self, fieldName):
		return self.getFieldObj(fieldName).type()

	### Change fields values

	def getConvertedFieldValue(self, fieldName, newValue):
		self.ensureFieldExists(fieldName)
		return self.fieldTypes[fieldName].castFunction(newValue)

	def setFieldType(self, fieldName, modelClass):
		if isinstance(self[fieldName], modelClass):
			return
		model = modelClass()
		model.copyFrom(self[fieldName])
		self[fieldName] = model

	### Copy objects

	def copyFrom(self, other):
		for key in other.fields:
			if self.fieldExist(key):
				self[key] = copy.deepcopy(other.fields[key])

	def createNewInstance(self):
		return type(self)()

	def __deepcopy__(self, *p):
		newMe = self.createNewInstance()
		for key in self.fields:
			newMe.fields[key] = copy.deepcopy(self.fields[key])
		return newMe

	### Access operators

	def __getitem__(self, fieldName):
		""" Get an field value. Overload [] operator """
		fieldName = str(fieldName)
		if not '.' in fieldName:
			self.ensureFieldExists(fieldName)
			return self.fields[fieldName]

		names = fieldName.split('.')
		model = self
		for prop in names:
			if isinstance(model, DataModel):
				model = model[prop]
			else:
				raise KeyError()
		return model

	def __setitem__(self, fieldName, newValue):
		""" Set value of a field. Overload [] affectation opeator """
		fieldName = str(fieldName)
		if not '.' in fieldName:
			self.fields[fieldName] = self.getConvertedFieldValue(fieldName, newValue)
		else:
			fieldName = fieldName.split('.')
			model = self['.'.join(fieldName[:-1])]
			if not isinstance(model, DataModel):
				raise KeyError
			model[fieldName[-1]] = newValue

	def __contains__(self, fieldName):
		""" Test if a field exit. Overload in operator """
		return str(fieldName) in self.fields

	def __iter__(self):
		""" Allow iteration through all fields """
		return self.fieldsList().__iter__()

	### Static functions

	@classmethod
	def getModelName(className):
		name = className.__name__
		if name.endswith('Model'):
			name = name[:-5]
		words = re.findall('[A-Z][^A-Z]*', name)
		name = '_'.join([w.lower() for w in words])

		return name