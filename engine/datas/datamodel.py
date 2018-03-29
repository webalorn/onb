class DataModel:
	"""
	Base class for data storgae

	raise: KeyError
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

	def fieldsList(self):
		return self.fields.keys()

	def fieldExist(self, fieldName):
		return fieldName in self.fieldTypes

	def copyFrom(self, other):
		for key in other.fields:
			if self.fieldExist(key):
				self[key] = other.fields[key]

	def getConvertedFieldValue(self, fieldName, newValue):
		if not fieldName in self.fieldTypes:
			raise KeyError()
		return self.fieldTypes[fieldName].castFunction(newValue)

	def setFieldType(self, fieldName, classname):
		if isinstance(self[fieldName], classname):
			return
		model = classname()
		model.copyFrom(self[fieldName])
		self[fieldName] = model

	### Access operators

	def __getitem__(self, fieldName):
		""" Get an field value. Overload [] operator """
		if not '.' in fieldName:
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
		return fieldName in self.fields

	def __iter__(self):
		""" Allow iteration through all fields """
		return self.fieldsList().__iter__()

	def __repr__(self):
		return str(self.fields)