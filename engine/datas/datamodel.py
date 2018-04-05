import re, copy, inspect

class DataModel:
	"""
	Base class for data storgae

	raise: KeyError

	type field name is reserved for the type of the model
	"""

	fieldTypes = None
	def getFields():
		"""A dictionary of all fields. Fields must inherit FieldValue"""
		return {}

	@classmethod
	def agregateAttr(cls, attrname):
		saveName = '_aggregate_saved_' + cls.__name__ + '_' + attrname 
		if hasattr(cls, saveName):
			return getattr(cls, saveName)

		attr = getattr(cls, attrname)
		if callable(attr):
			attr = attr()
		for base in cls.__bases__:
			if hasattr(base, 'agregateAttr') and hasattr(base, attrname):
				subattr = base.agregateAttr(attrname)
				if isinstance(attr, list):
					attr += subattr
				else:
					attr = {**subattr, **attr}
		setattr(cls, saveName, attr)
		return attr

	@classmethod
	def getFieldTypes(cls):
		cls.fieldTypes = cls.agregateAttr('getFields')
		return cls.fieldTypes

	def __init__(self, populateWith = None):
		""" All properties must start with 'field' or '_' """
		self.fields = {}
		self.getFieldTypes()
		for fieldName in self.fieldTypes:
			self.fields[fieldName] = self.fieldTypes[fieldName].defaultValue()

		if populateWith:
			self.populate(populateWith)

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

	def populate(self, datas):
		from .populate import PopulateManager
		return PopulateManager().populate(self, datas)

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

	@classmethod
	def isReservedField(cls, attr):
		return attr[:5] == 'field' or attr[:1] == '_' or hasattr(cls, attr)

	def __getattr__(self, attr):
		if not self.isReservedField(attr):
			return self.fields[attr]
		raise AttributeError

	def __setattr__(self, attr, value):
		if self.isReservedField(attr):
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
		if '.' in fieldName:
			return self.callSubModel(fieldName, 'get', default=None)
		if str(fieldName) in self.fields:
			return self[fieldName]
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