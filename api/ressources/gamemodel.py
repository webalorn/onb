from flask_restful import Resource, reqparse, marshal, marshal_with
from sqldb.models.gameobject import sqlModels
from api.common.errors import *
from api.fields.gamemodel import *
import flask_jwt_extended as fjwt
import onb, peewee


### Endpoints

@onb.api.resource('/model/<model:modelclass>')
class Model(Resource):
	pass

@onb.api.resource('/model/<model:modelclass>/<int:id>')
class ModelWithId(Resource):
	@fjwt.jwt_optional
	@marshal_with(model_fields)
	def get(self, modelclass, id):
		return modelclass.get(id=id)