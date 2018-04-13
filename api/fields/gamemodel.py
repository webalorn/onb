from flask_restful import fields, reqparse
from engine.storage.encoder import ModelEncoder
import flask_jwt_extended as fjwt
import copy

class ModelField(fields.Raw):
	def format(self, value):
		return ModelEncoder.encode(value)

class ModelSchemaField(fields.Raw):
	def format(self, value):
		""" Return the model schema if requested """
		parser = reqparse.RequestParser()
		parser.add_argument('schema', type=bool)
		args = parser.parse_args()

		if args['schema']:
			return ModelEncoder.encodeTypes(value)
		return None


model_fields = {
	'id': fields.Integer,
	'owner_id': fields.String,
	'type': fields.String,
	'is_official': fields.Boolean,
	'is_public': fields.Boolean,
	'is_generated': fields.Boolean,
	'model': ModelField,
	'schema': ModelSchemaField(attribute='model')
}