from flask_restful import Resource, reqparse, marshal, marshal_with, inputs
from sqldb.models.user import User as sqlUser
from api.common.errors import *
from api.fields.user import *
from api.common.auth import jwt_anonymous_user
import flask_jwt_extended as fjwt
import onb

### Parsers

def authParser():
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True)
	parser.add_argument('password', type=str, required=True)
	return parser

def createParser():
	return authParser().copy()

### Endpoints

@onb.api.resource('/user')
class User(Resource):
	@classmethod
	def getNewUserFields(cls):
		args = createParser().parse_args()
		username = args['username'].strip()
		password = sqlUser.hashPassword(args['password'])

		if not username:
			raise BadRequestError
		if sqlUser.select().where(sqlUser.username == args['username']):
			raise UserAlreadyExistsError
		return username, password

	@marshal_with(auth_user_fields)
	def post(self):
		username, password_hash = self.getNewUserFields()
		user = sqlUser.create(username=username, password_hash=password_hash)
		return user

	@fjwt.jwt_required
	@marshal_with(auth_user_fields)
	def get(self):
		user = fjwt.get_current_user()
		if user:
			return user
		raise NotFoundError

@onb.api.resource('/user/anonymous')
class AnonymousUser(Resource):
	@marshal_with(auth_user_fields)
	def post(self):
		""" Create a new anonymous user """
		user = sqlUser.create(username=None, password_hash=None)
		return user

	@marshal_with(auth_user_fields)
	@jwt_anonymous_user
	def put(self):
		""" Create a real account from an anonymous user """
		user = fjwt.get_current_user()
		username, password_hash = User.getNewUserFields()
		user.username = username
		user.password_hash = password_hash
		user.save()
		return user

@onb.api.resource('/user/<int:id>')
class UserWithId(Resource):
	@fjwt.jwt_optional
	@marshal_with(user_fields)
	def get(self, id):
		return sqlUser.get(id=id)

@onb.api.resource('/user/auth')
class UserAuth(Resource):
	@marshal_with(auth_user_fields)
	def get(self):
		args = authParser().parse_args()
		password = sqlUser.hashPassword(args['password'])

		try:
			user = sqlUser.get(username=args['username'])
			if not user.verifyPassword(args['password']):
				raise UserAuthError
		except NotFoundError:
			raise UserAuthError

		return user