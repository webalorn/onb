import re, copy, inspect

class DataModel:
	"""
	Base class for data storgae

	raise: KeyError

	type field name is reserved for the type of the model
	"""


	def getFields(self):
		""" Return a dictionary of all fields. Fields must inherit FieldValue """
		return {}

	def _getAllFields(self, actualClass=None):
		if actualClass == None:
			actualClass = self.__class__
		fields = {}
		for cls in reversed(inspect.getmro(actualClass)):
			if issubclass(cls, DataModel):
				subFields = cls.getFields(self)
				for key in subFields:
					fields[key] = subFields[key]
		return fields

	def __init__(self):
		""" All properties must start with 'field' or '_' """
		self.fields = {}
		self.fieldTypes = self._getAllFields()
		for fieldName in self.fieldTypes:
			self.fields[fieldName] = self.fieldTypes[fieldName].defaultValue

	def __repr__(self):
		return str(self.fields)

	def callSubModel(self, fieldName, fctName, *p, **pn):
		""" Call a function on a sub-model. Used when the fieldname contain '.'.
		The function must take fielName as first parameter """
		fieldName = fieldName.split('.')
		model = self['.'.join(fieldName[:-1])]
		if not isinstance(model, DataModel):
			raise KeyError()
		return getattr(model, fctName)(fieldName[-1], *p, **pn)

	### Get Fields and FieldClass 

	def fieldsList(self):
		return self.fields.keys()

	def fieldExist(self, fieldName):
		return fieldName in self.fieldTypes

	def ensureFieldExists(self, fieldName):
		if not fieldName in self.fields:
			raise KeyError("Field {0} doesn't exist".format(fieldName))

	def getFieldObj(self, fieldName):
		if '.' in fieldName:
			return self.callSubModel(fieldName, 'getFieldObj')
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

	def __getattr__(self, attr):
		return self.fields[attr]

	def __setattr__(self, attr, value):
		if attr[:5] == 'field' or attr[:1] == '_':
			super().__setattr__(attr, value)
		else:
			self[attr] = value

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
			callSubModel(fieldName, '__setitem__')

	def __contains__(self, fieldName):
		""" Test if a field exit. Overload in operator """
		return str(fieldName) in self.fields

	def __iter__(self):
		""" Allow iteration through all fields """
		return self.fieldsList().__iter__()

	def get(self, fieldName, default=None):
		try:
			return self[fieldName]
		except:
			return default

	### Static functions

	@classmethod
	def getModelName(classObj):
		name = classObj.__name__
		if name.endswith('Model'):
			name = name[:-5]
		words = re.findall('[A-Z][^A-Z]*', name)
		name = '_'.join([w.lower() for w in words])

		return name


	### Storage

	_storageLocation = None # Only used by StorageManager
	def save(self):
		from ..storage.manager import StorageManager
		StorageManager().save(self)