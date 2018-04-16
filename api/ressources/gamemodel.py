from flask_restful import Resource, reqparse, marshal, marshal_with, request
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

def getSearchArgsParser():
	parser = reqparse.RequestParser()
	parser.add_argument('search', type=str, required=True)
	return parser

def modelListGetFilterArgsAndClause(modelclass):
	args = modelListFilterParser().parse_args()
	
	whereClause = (modelclass.is_public == True) | (modelclass.owner_id == fjwt.get_jwt_identity())
	if args['only_official']:
		whereClause = whereClause & (modelclass.is_official == True)

	return args, whereClause

### Endpoints

@onb.api.resource('/model/<model:modelclass>/page/<int:pageId>', '/model/<model:modelclass>')
class ModelPages(Resource):
	@marshal_with(model_summary)
	@fjwt.jwt_optional
	def get(self, modelclass, pageId=1):
		args, whereClause = modelListGetFilterArgsAndClause(modelclass)
		return list(modelclass.select()
				.paginate(pageId, args['pagination'])
				.where(whereClause))

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

@onb.api.resource('/model/<model:modelclass>/search', '/model/<model:modelclass>/search/page/<int:pageId>')
class ModelSearch(Resource):
	@fjwt.jwt_optional
	@marshal_with(model_summary)
	def get(self, modelclass, pageId=1):
		searchArgs = getSearchArgsParser().parse_args()

		args, whereClause = modelListGetFilterArgsAndClause(modelclass)
		try:
			return list(modelclass.search(searchArgs['search'])
				.paginate(pageId, args['pagination'])
				.where(whereClause))
		except peewee.OperationalError:
			raise BadRequestError

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