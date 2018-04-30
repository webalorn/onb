from flask_restful import fields, reqparse
from engine.storage.encoder import ModelEncoder
import flask_jwt_extended as fjwt

class ModelField(fields.Raw):
	def format(self, value):
		return ModelEncoder.encode(value)

class ShortModelField(fields.Raw):
	def format(self, model):
		return {prop: model[prop] for prop in model.getExposedFields()}

model_base_infos = {
	'id': fields.Integer,
	'owner_id': fields.Integer,
	'type': fields.String,
	'is_official': fields.Boolean,
	'is_public': fields.Boolean,
	'is_generated': fields.Boolean,
}

model_summary = {
	**model_base_infos,
	'model': ShortModelField,
}

model_fields = {
	**model_base_infos,
	'model': ModelField,
}