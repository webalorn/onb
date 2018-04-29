from flask_restful import fields, reqparse
from engine.storage.encoder import ModelEncoder
import flask_jwt_extended as fjwt

class ModelField(fields.Raw):
	def format(self, value):
		return ModelEncoder.encode(value)

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
	'model': {
		'name': fields.String,
		'summary': fields.String,
		'description': fields.String,
		"alignment": fields.String,
		"race": fields.String,
		"subrace": fields.String,
		"universe": fields.String,
		"battleground": fields.String,
		"unit_type": fields.String,
		"cost": fields.Integer,
		"_type": fields.String,
	},
}

model_fields = {
	**model_base_infos,
	'model': ModelField,
}