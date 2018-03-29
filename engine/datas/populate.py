from .datamodel import DataModel

class PopuplateManager:
	def __init__(self):
		# Import here to avoir circular reference
		from ..modelslist import modelsList
		self.modelsList = modelsList

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
		if 'type' in datas:
			model.setType(datas['type'])
			datas.pop('type')

		for key in datas:
			model.ensureFieldExists(key)
			if isinstance(datas[key], dict):
				self._populateModel(model[key], datas[key])
			else:
				model[key] = datas[key]

	def populate(self, model, datas):
		self.normalizeDatas(datas)
		self._populateModel(model, datas)