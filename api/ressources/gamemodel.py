from flask_restful import Resource, reqparse, marshal, marshal_with, request
import flask_jwt_extended as fjwt
from sqldb.models.gameobject import sqlModels
from engine.storage.encoder import ModelEncoder
from api.common.errors import *
from api.fields.gamemodel import *
import onb, peewee

def getFilterArgs():
	parser = reqparse.RequestParser()
	parser.add_argument('page', type=int, default=1)
	parser.add_argument('pagination', type=int, default=20)
	parser.add_argument('only_official', type=bool, default=True)
	parser.add_argument('public_only', type=bool, default=True)
	parser.add_argument('owner', type=int, nullable=True, default=None)
	parser.add_argument('fields', type=dict, default={})

	args = parser.parse_args()
	if (args['pagination'] < 1):
		raise BadRequestError('pagination value must be at least 1')
	if (args['pagination'] > 100):
		raise BadRequestError('pagination value must be at most 100')
	return args

def getSearchArgs():
	searchParser = reqparse.RequestParser()
	searchParser.add_argument('search', type=str, required=True)
	return searchParser.parse_args()

def getModelArgs():
	parser = reqparse.RequestParser()
	parser.add_argument('model', type=dict, default={})
	parser.add_argument('is_public', type=bool, nullable=True, default=None)

	if fjwt.current_user.is_admin:
		parser.add_argument('is_official', type=bool, nullable=True, default=None)

	return {key:val for key, val in parser.parse_args().items() if val != None}

def modelListGetFilterArgsAndClause(modelclass):
	args = getFilterArgs()
	
	whereClause = True
	if args['public_only']:
		whereClause = whereClause & (modelclass.is_public == True)
	if args['only_official']:
		whereClause = whereClause & (modelclass.is_official == True)
	if args['owner']:
		whereClause = whereClause & (modelclass.owner_id == args['owner'])
	for name, val in args['fields'].items():
		whereClause = whereClause & (getattr(modelclass, name) == val)

	return args, whereClause

"""
Model Endpoints
"""

@onb.api.resource('/model/<model:modelclass>')
class Model(Resource):
	@marshal_with(model_summary)
	def get(self, modelclass, pageId=1):
		args, whereClause = modelListGetFilterArgsAndClause(modelclass)
		return list(modelclass.select()
				.paginate(args['page'], args['pagination'])
				.where(whereClause))
	
	@fjwt.jwt_required
	@marshal_with(model_fields)
	def post(self, modelclass):
		model = modelclass.create(
			owner_id = fjwt.current_user.id,
			**getModelArgs(),
		)
		return model

# Search a model

@onb.api.resource('/model/<model:modelclass>/search')
class ModelSearch(Resource):
	@marshal_with(model_summary)
	def get(self, modelclass, pageId=1):
		searchArgs = getSearchArgs()

		args, whereClause = modelListGetFilterArgsAndClause(modelclass)
		return list(modelclass.search(searchArgs['search'])
			.paginate(args['page'], args['pagination'])
			.where(whereClause))

# Access a particular model

@onb.api.resource('/model/<model:modelclass>/<int:id>')
class ModelWithId(Resource):
	@marshal_with(model_fields)
	def get(self, modelclass, id):
		return modelclass.get(id=id)

	@fjwt.jwt_required
	@marshal_with(model_fields)
	def put(self, modelclass, id):
		model = modelclass.get(id=id, owner_id = fjwt.current_user.id)
		args = getModelArgs()
		try:
			model.model.populate(args['model'])
		except:
			raise BadRequestError()

		del args['model']
		for argname, argval in args.items():
			setattr(model, argname, argval)
		model.save()

		return model

	@fjwt.jwt_required
	def delete(self, modelclass, id):
		model = modelclass.get(id=id, owner_id = fjwt.current_user.id)
		model.delete_instance()
		return None

# Get models schemas

@onb.api.resource('/model/<model:modelclass>/schemas')
class ModelSchemas(Resource):
	def get(self, modelclass):
		return {
			"model": modelclass.modelClass,
			"schemas": ModelEncoder.encodeSchemas(modelclass.modelClass),
		}