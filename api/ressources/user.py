from flask_restful import Resource, reqparse, marshal_with, inputs, request
from sqldb.models.user import User as sqlUser
from sqldb.models.user import Friendship
from api.common.errors import *
from api.fields.user import *
from api.common.auth import jwt_anonymous_user
import flask_jwt_extended as fjwt
from api.common.parser import ExtendedParser, checkPagination
import onb, datetime, random

### Parsers

def authParser():
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True)
	parser.add_argument('password', type=str, required=True)
	return parser

def createParser():
	return authParser().copy()

def parseSearchArgs():
	parser = reqparse.RequestParser()
	parser.add_argument('search', type=str, required=True)
	parser.add_argument('page', type=int, default=1)
	parser.add_argument('pagination', type=int, default=20)

	args = parser.parse_args()
	checkPagination(args['pagination'], maxi=20)
	return args

def parseUserProfile(vals):
	parser = ExtendedParser()
	parser.add_argument('avatar_id', type=int)
	parser.add_argument('description', type=str)
	parser.add_argument('birthdate', type=lambda x : datetime.datetime.strptime(x, "%d-%m-%Y")),
	parser.add_argument('country', type=str)
	parser.add_argument('gender', type=str, choices=[None, 'M', 'F'])
	parser.add_argument('first_name', type=str)
	parser.add_argument('last_name', type=str)
	return parser.parse_args_from(vals)

def parseUserSettings(vals):
	parser = ExtendedParser()
	parser.add_argument('language', type=str, choices=onb.conf.langs)
	parser.add_argument('i12n_editor', type=bool)
	return parser.parse_args_from(vals)

def parseUserDatas():
	parser = reqparse.RequestParser()
	parser.add_argument('profile', type=parseUserProfile, default={})
	parser.add_argument('settings', type=parseUserSettings, default={})
	return parser.parse_args()
	return args

def parseChangePassword():
	parser = reqparse.RequestParser()
	parser.add_argument('password', type=str)
	parser.add_argument('new_password', type=str)
	return parser.parse_args()

### Common functions

def getNewUserFields():
	args = createParser().parse_args()
	username = args['username'].strip()
	password = sqlUser.hashPassword(args['password'])

	if not username:
		raise BadRequestError
	if sqlUser.usernameExists(args['username']):
		raise UserAlreadyExistsError
	return username, password

def updateUser(user):
	user.updateFrom(parseUserDatas())
	return user

### Endpoints

@onb.api.resource('/user')
class User(Resource):
	@marshal_with(auth_user_fields)
	def post(self):
		username, password_hash = getNewUserFields()
		return updateUser(sqlUser.create(username=username, password_hash=password_hash))

	@fjwt.jwt_required
	@marshal_with(auth_user_fields)
	def get(self):
		user = fjwt.get_current_user()
		if user:
			return user
		raise NotFoundError

	@fjwt.jwt_required
	@marshal_with(auth_user_fields)
	def put(self):
		return updateUser(fjwt.get_current_user())

@onb.api.resource('/user/username_available')
class UsernameAvailable(Resource):
	def get(self):
		username = request.get_json()
		if sqlUser.usernameExists(username):
			suggest = [username + str(random.randint(1, 999)) for k in range(5)]
			suggest = [username for username in suggest if not sqlUser.usernameExists(username)]

			return {'available': False, 'suggestions': suggest}, 409
		return {'available': True}

@onb.api.resource('/user/search')
class SearchUser(Resource):
	@marshal_with(user_fields_short)
	def get(self):
		args = parseSearchArgs()
		return list(sqlUser.search(args['search'])
			.paginate(args['page'], args['pagination']))

@onb.api.resource('/user/anonymous')
class AnonymousUser(Resource):
	@marshal_with(auth_user_fields)
	def get(self):
		""" Create a new anonymous user """
		return sqlUser.create(username=None, password_hash=None)

	@marshal_with(auth_user_fields)
	@jwt_anonymous_user
	def post(self):
		""" Create a real account from an anonymous user """
		user = fjwt.get_current_user()
		username, password_hash = getNewUserFields()
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

	@fjwt.jwt_required
	def delete(self):
		fjwt.get_current_user().revoke_all_jwt()

	@fjwt.jwt_required
	def post(self):
		args = parseChangePassword()
		user = fjwt.get_current_user()
		if not user.verifyPassword(args['password']):
			raise UserAuthError
		user.setPassword(args['new_password'])
		user.save()

@onb.api.resource('/user/friend/<int:friend_id>')
class UserFriends(Resource):
	@fjwt.jwt_required
	def post(self, friend_id):
		if friend_id == fjwt.get_current_user().id:
			raise NotFoundError
		try:
			sqlUser.get(id=friend_id)
		except:
			raise NotFoundError
		Friendship.get_or_create(follower_id=fjwt.get_current_user().id, friend_id=friend_id)

	@fjwt.jwt_required
	def delete(self, friend_id):
		try:
			friend = Friendship.get(follower_id=fjwt.get_current_user().id, friend_id=friend_id).delete_instance()
		except:
			raise NotFoundError