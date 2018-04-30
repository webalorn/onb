from ..datas.datamodel import DataModel
from ..datas.structfields import *
from ..datas.fieldvalues import *
from ..modelslist import getModelByName
from ..datas.populate import PopulateManager
import inspect, onb

class SchemaEncode:
	def __init__(self, modelObj):
		self.schemas = {}
		self.encode(modelObj)

	def encode(self, obj):
		"""
			$obj is a reference to an object
		"""
		if isinstance(obj, str): # In case of a model identifier
			obj = getModelByName(obj)

		if isinstance(obj, DataModel):
			return self.encode(type(obj))
		elif inspect.isclass(obj) and issubclass(obj, DataModel):
			name = obj.getModelName()
			if not name in self.schemas:
				self.schemas[name] = {
					'type': 'model',
					'model_name': obj.getModelName(),
					'submodels': self.encodeSubModel(obj),
					'fields':  {key : self.encode(field) for key, field in obj.getFieldTypes().items()}
				}
			return '$' + name
		elif isinstance(obj, FieldValue):
			# List and dict -> direct recall with fieldssharedtype
			# Object -> recall with the object class
			# otherwise, return string type
			if isinstance(obj, DictField):
				return {
					'type': 'dict',
					'items': self.encode(obj.classParams[0]), # [0] -> fieldsSharedType
					**({'keysIn': obj.keysIn} if obj.keysIn else {})
				}
			elif isinstance(obj, ListField):
				return {
					'type': 'list',
					'items': self.encode(obj.classParams[0]), # [0] -> fieldsSharedType
				}
			elif isinstance(obj, ClassField):
				return self.encode(obj.type())
			else:
				# return field class name in lower case, without "Field" at the end
				return {
					'type': obj.__class__.__name__[:-5].lower(),
					**{
						prop : getattr(obj, prop)
						for prop in obj.fieldProperties
						if getattr(obj, prop) != getattr(obj.__class__, prop)
					}
				}

		return "<unknown>"

	def encodeSubModel(self, modelclass):
		subs = []
		for subClass in modelclass.__subclasses__():
			subs.append(self.encode(subClass))
			subs += self.encodeSubModel(subClass)
		return subs

	def get(self):
		return self.schemas

class ModelEncoder:
	""" Provides functions for json <-> models convertions """
	schemasEncoded = {}
	
	@classmethod
	def encode(cls, model):
		if isinstance(model, DataModel):
			modelName = model.getModelName()
			datas = {}

			for field in model.fields:
				fieldValue = model.fields[field]
				fieldValue = model.getFieldObj(field).getDbValue(fieldValue)

				if fieldValue != None:
					datas[field] = cls.encode(fieldValue)
					# Remove key 'type' if it is the default type
					if isinstance(datas[field], dict) and '_type' in datas[field]:
						if getModelByName(datas[field]['_type']) == model.getFieldType(field):
							del datas[field]['_type']

			if isinstance(model, ListModel):
				datas = [datas[str(key)] for key in model.getSortedKeys()]
			else:
				datas["_type"] = modelName
			return datas
		return model

	@classmethod
	def linearize(cls, datas):
		oneline = {}
		for key in datas:
			if isinstance(datas[key], dict):
				sub_oneline = cls.linearize(datas[key])
				for key2 in sub_oneline:
					oneline[key + '.' + key2] = sub_oneline[key2]
			else:
				oneline[key] = datas[key]
		return oneline

	@classmethod
	def decode(cls, datas):
		modelName = 'creature'
		if '_type' in datas:
			modelName = datas['_type']
		modelClass = getModelByName(modelName)
		model = modelClass()
		PopulateManager().populate(model, datas)
		return model

	@classmethod
	def encodeSchemas(cls, obj):
		schemaName = obj if type(obj) == str else obj.getModelName()
		if not schemaName in cls.schemasEncoded or onb.conf.debug:
			cls.schemasEncoded[schemaName] = SchemaEncode(obj)
		return cls.schemasEncoded[schemaName].get()

	"""@classmethod
	def encodeTypes(cls, obj):
		# return {'type':'model', 'fields': ...}
		if isinstance(obj, str): # In case of a model identifier
			obj = getModelByName(obj)

		if isinstance(obj, DataModel):
			return cls.encodeTypes(type(obj))
		elif inspect.isclass(obj) and issubclass(obj, DataModel):
			datas = {'type':'model', 'model_name': obj.getModelName()}
			fields = obj.getFieldTypes()
			datas['fields'] = {key:cls.encodeTypes(fields[key]) for key in fields}
			return datas
		elif isinstance(obj, FieldValue):
			# List and dict -> direct recall with fieldssharedtype
			# Object -> recall with the object class
			# otherwise, return string type
			if isinstance(obj, DictField):
				datas = {'type':'dict', 'fieldsType': cls.encodeTypes(obj.classParams[0])} # [0] -> fieldsSharedType
				if obj.keysIn:
					datas['keysIn'] = obj.keysIn
				return datas
			elif isinstance(obj, ListField):
				return {'type':'list', 'fieldsType': cls.encodeTypes(obj.classParams[0])} # [0] -> fieldsSharedType
			elif isinstance(obj, ClassField):
				return cls.encodeTypes(obj.type())
			else:
				# return field class name in lower case, without "Field" at the end
				type_name = obj.__class__.__name__[:-5].lower()
				datas = {'type': type_name}

				# Property name -> default value
				for prop in obj.fieldProperties:
					if getattr(obj, prop) != getattr(obj.__class__, prop):
						datas[prop] = getattr(obj, prop)
				return datas

		return "<unknown>"""