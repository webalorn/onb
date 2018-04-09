from ..datas.datamodel import DataModel
from ..datas.fieldvalues import *

"""
Allowed Fields:
	-> BoolField (optional default value)
	-> IntField (optional default value)
	-> StringField (optional default value)
	-> FloatField (optional default value)

	-> ClassField (required model type) # The subclasses of the model are allowed
	-> DictField (required fields values type)
	-> ListField (required fields values type)
	-> ForeignKeyField (required model identifier)
"""

class BaseGameModel(DataModel):
	storable = False # Will this model  be directly stored in the database ?
	exposedFields = [] # Field added in the databse entry

	@classmethod
	def getExposedFields(cls):
		return cls.agregateAttr('exposedFields')

class DbStorableModel(DataModel): # won't be directly stored, despite of 'storable=True' because doesn't inherit 'BaseGameModel'
	"""
	Define common fields for extra-informations
	It's not required to use this model to create storable models
	Must be before 'BaseGameModel' in inheritance list
	"""
	def getFields():
		return {
			'name': StringField(),
			'summary': StringField(),
			'description': StringField(),
			'image_id': IntField(),
		}

	exposedFields = ['name', 'summary', 'description', 'image_id']
	storable = True


class GameEntityModel(BaseGameModel):
	def getFields():
		print("GET fields")
		return {
			'name': StringField(),
			'alignment': StringField(default="neutral", helperList="alignment"),
			'race': StringField(helperList="race"),

			'health': IntField(1),
			'size': IntField(1),
			'protection': ClassField('protection', optional=True),
		}
	exposedFields = ['name', 'race', 'alignment']