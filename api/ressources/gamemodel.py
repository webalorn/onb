from flask_restful import Resource, reqparse, marshal, marshal_with
from flask import request
import flask_jwt_extended as fjwt
from sqldb.models.gameobject import sqlModels
from api.common.errors import *
from api.fields.gamemodel import *
import onb, peewee

modelsPagination = 20

### Endpoints

@onb.api.resource('/model/<model:modelclass>/page/<int:pageId>', '/model/<model:modelclass>')
class ModelPages(Resource):
	@marshal_with(model_summary)
	def get(self, modelclass, pageId=1):
		return list(modelclass.select().paginate(pageId, modelsPagination))

@onb.api.resource('/model/<model:modelclass>')
class Model(Resource):
	@fjwt.jwt_required
	@marshal_with(model_fields)
	def post(self, modelclass):
		model = modelclass.create(
			owner_id = fjwt.get_jwt_identity(),
			model=request.get_json()
		)
		return model

@onb.api.resource('/model/<model:modelclass>/<int:id>')
class ModelWithId(Resource):
	@marshal_with(model_fields)
	def get(self, modelclass, id):
		return modelclass.get(id=id)

	@fjwt.jwt_required
	@marshal_with(model_fields)
	def put(self, modelclass, id):
		model = modelclass.get(id=id, owner_id = fjwt.get_jwt_identity())
		model.model.populate(request.get_json())
		model.save()
		return model