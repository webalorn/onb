from flask_restful import fields
from .common_fields import *

class GameConfigField(fields.Raw):
	""" Use only when it's sure that the value already have the correct format """
	def format(self, value):
		exclude = ['table']
		return {key:val for key, val in value.items() if not key in exclude}

config_fields = {
	'langs': AnyFields,
	'searchEnabled': fields.Boolean,
	'anonymousLogin': fields.Boolean,
	'debug': fields.Boolean,
	'testingMode': fields.Boolean,
	'game': GameConfigField,
}