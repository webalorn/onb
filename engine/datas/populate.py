from .datamodel import DataModel
from ..modelslist import getModelByName
import copy

class PopulateManager:
	def __init__(self):
		# Import here to avoir circular reference
		from ..modelslist import modelsList
		self.modelsList = modelsList
		self.reservedFields = ['type']

	def convertDatas(self, datas):
		if isinstance(datas, list):
			datas = {key:datas[key] for key in range(len(datas))}
		if isinstance(datas, dict):
			newDatas = {}
			for key in datas:
				newDatas[str(key)] = self.convertDatas(datas[key])
			datas = newDatas
		return datas

	def normalizeDatas(self, datas):
		if isinstance(datas, dict):

			recursiveKeys = {key : datas[key] for key in datas if '.' in key}
			for key in recursiveKeys:
				datas.pop(key)

			for key in recursiveKeys:
				words = key.split('.')
				if not words[0] in datas or not isinstance(datas[words[0]], dict):
					datas[words[0]] = {}
				datas[words[0]]['.'.join(words[1:])] = recursiveKeys[key]
			
			for key in datas:
				self.normalizeDatas(datas[key])

	def _populateModel(self, model, datas):
		# Not intended for direct use by external code

		for key in datas:
			if not key in self.reservedFields:
				model.ensureFieldExists(key)
				if isinstance(datas[key], dict):
					if 'type' in datas[key]:
						model.setFieldType(key, getModelByName(datas[key]['type']))
					self._populateModel(model[key], datas[key])
				else:
					model[key] = datas[key]

	def populate(self, model, datas):
		datas = copy.deepcopy(datas)
		datas = self.convertDatas(datas)
		self.normalizeDatas(datas)
		self._populateModel(model, datas)
		return model