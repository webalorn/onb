from flask_restful import Resource, reqparse, marshal, marshal_with
from flask import request
import flask_jwt_extended as fjwt
from sqldb.models.gameobject import sqlModels
from api.common.errors import *
from api.fields.gamemodel import *
import onb, peewee

def modelListFilterParser():
	parser = reqparse.RequestParser()
	parser.add_argument('pagination', type=int, default=20)
	parser.add_argument('only_official', type=bool, default=False)
	return parser

### Endpoints

@onb.api.resource('/model/<model:modelclass>/page/<int:pageId>', '/model/<model:modelclass>')
class ModelPages(Resource):
	@marshal_with(model_summary)
	@fjwt.jwt_optional
	def get(self, modelclass, pageId=1):
		args = modelListFilterParser().parse_args()
		req = (modelclass.select()
				.paginate(pageId, args['pagination'])
				.where((modelclass.is_official == True) | (modelclass.is_official == args['only_official']))
				.where((modelclass.is_public == True) | (modelclass.owner_id == fjwt.get_jwt_identity()))
		)

		return list(req)

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
	@fjwt.jwt_optional
	@marshal_with(model_fields)
	def get(self, modelclass, id):
		model = modelclass.get(id=id)
		if not model.is_public and model.owner_id != fjwt.get_jwt_identity():
			raise NotFoundError
		return model

	@fjwt.jwt_required
	@marshal_with(model_fields)
	def put(self, modelclass, id):
		model = modelclass.get(id=id, owner_id = fjwt.get_jwt_identity())
		try:
			model.model.populate(request.get_json())
		except:
			raise BadRequestError()
		model.save()
		return model

	@fjwt.jwt_required
	def delete(self, modelclass, id):
		model = modelclass.get(id=id, owner_id = fjwt.get_jwt_identity())
		model.delete_instance()
		return None