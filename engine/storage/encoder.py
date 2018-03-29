from ..datas.datamodel import DataModel

class ModelEncoder:
	def encode(self, model):
		if isinstance(model, DataModel):
			model = model.fields
			for field in model:
				model[field] = self.encode(model[field])
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