from peewee import TextField

class GameModelField(TextField):
	_modelObj = None
	def _getModelObj(self):
		print("Try to get model")