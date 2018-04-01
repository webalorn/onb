from ..datas.datamodel import DataModel
from ..datas.structfields import *
from ..datas.fieldvalues import *
from ..modelslist import getModelByName
from ..datas.populate import PopuplateManager
import inspect

class ModelEncoder:
	""" Provides functions for json <-> models convertions """

	def encode(self, model):
		if isinstance(model, DataModel):
			modelName = model.getModelName()
			datas = {}

			for field in model.fields:
				datas[field] = self.encode(model.fields[field])
				# Remove key 'type' if it is the default type
				if isinstance(datas[field], dict) and 'type' in datas[field]:
					if getModelByName(datas[field]['type']) == model.getFieldType(field):
						del datas[field]['type']

			datas["type"] = modelName
			return datas
		return model

	def linearize(self, datas):
		oneline = {}
		for key in datas:
			if isinstance(datas[key], dict):
				sub_oneline = self.linearize(datas[key])
				for key2 in sub_oneline:
					oneline[key + '.' + key2] = sub_oneline[key2]
			else:
				oneline[key] = datas[key]
		return oneline

	def decode(self, datas):
		modelName = 'creature'
		if 'type' in datas:
			modelName = datas['type']
		modelClass = getModelByName(modelName)
		model = modelClass()
		PopuplateManager().populate(model, datas)
		return model

	def encodeTypes(self, obj):
		"""
			return {'type':'model', 'fieldsType': ...}
		"""
		if isinstance(obj, DataModel):
			return self.encodeTypes(type(obj))
		elif inspect.isclass(obj) and issubclass(obj, DataModel):
			datas = {'type':'model', 'model_name': obj.getModelName()}
			fields = obj._getAllFields(object(), obj)
			datas['fieldsType'] = {key:self.encodeTypes(fields[key]) for key in fields}
			return datas
		elif isinstance(obj, FieldValue):
			# List and dict -> direct recall with fieldssharedtype
			# Object -> recall with the object class
			# otherwise, return string type
			if isinstance(obj, DictField):
				return {'type':'dict', 'fieldsType': self.encodeTypes(obj.classParams[0])} # [0] -> fieldsSharedType
			elif isinstance(obj, ListField):
				return {'type':'list', 'fieldsType': self.encodeTypes(obj.classParams[0])} # [0] -> fieldsSharedType
			elif isinstance(obj, ClassField):
				return self.encodeTypes(obj.type())
			else:
				# return field class name in lower case, without "Field" at the end
				type_name = obj.__class__.__name__[:-5].lower()
				datas = {'type': type_name}

				# Property name -> default value
				properties = {'values': None, 'min': None, 'max': None, 'helperList': None, 'generated': False}
				for prop in properties:
					if getattr(obj, prop) != properties[prop]:
						datas[prop] = getattr(obj, prop)
				return datas

		return "<unknown>"