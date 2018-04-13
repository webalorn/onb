from flask_restful import Resource, reqparse, marshal, marshal_with
from sqldb.models.user import User as sqlUser
from api.common.errors import *
from api.fields.user import *
import flask_jwt_extended as fjwt
import onb

### Parsers

def authParser():
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True)
	parser.add_argument('password', type=str, required=True)
	return parser

def createParser():
	return authParser()

### Endpoints

@onb.api.resource('/user')
class User(Resource):
	@marshal_with(auth_user_fields)
	def post(self):
		args = createParser().parse_args()
		password = sqlUser.hashPassword(args['password'])

		if sqlUser.select().where(sqlUser.username == args['username']).exists():
			raise UserAlreadyExistsError()

		user = sqlUser.create(username=args['username'], autoSave=False, password_hash=password)
		return user

@onb.api.resource('/user/<int:id>')
class UserWithId(Resource):
	@fjwt.jwt_optional
	def get(self, id):
		user = fjwt.get_current_user()
		if user and user.id == id:
			return marshal(user, auth_user_fields)
		return marshal(sqlUser.get(id=id), user_fields)

@onb.api.resource('/user/auth')
class UserAuth(Resource):
	@marshal_with(auth_user_fields)
	def get(self):
		args = authParser().parse_args()
		password = sqlUser.hashPassword(args['password'])

		try:
			user = sqlUser.get(username=args['username'])
			if not user.verifyPassword(args['password']):
				raise UserAuthError()
		except NotFoundError:
			raise UserAuthError()

		return user