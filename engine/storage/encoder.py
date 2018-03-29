from ..datas.datamodel import DataModel
from ..modelslist import getModelByName
from ..datas.populate import PopuplateManager

class ModelEncoder:
	def encode(self, model):
		if isinstance(model, DataModel):
			modelName = model.getModelName()
			datas = model.fields

			for field in datas:
				datas[field] = self.encode(datas[field])
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