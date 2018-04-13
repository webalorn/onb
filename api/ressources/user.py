from flask_restful import Resource, reqparse
from sqldb.models.user import User as sqlUser
from api.common.errors import *
import onb

print("user")

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('datas')


def authParser():
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True)
	parser.add_argument('password', type=str, required=True)
	return parser

def createParser():
	return authParser()

@onb.api.route('/user')
class User(Resource):
	def post(self):
		args = createParser().parse_args()
		password = sqlUser.hashPassword(args['password'])

		if sqlUser.select().where(sqlUser.username == args['username']).exists():
			raise UserAlreadyExistsError()

		sqlUser.create(username=args['username'], autoSave=False, password_hash=password)
		return {"test": "created"}

@onb.api.route('/user/auth')
class UserAuth(Resource):
	def get(self):
		args = authParser().parse_args()
		password = sqlUser.hashPassword(args['password'])

		try:
			user = sqlUser.get(username=args['username'])
			if not user.verifyPassword(args['password']):
				raise UserAuthError()
		except sqlUser.DoesNotExist:
			raise UserAuthError()

		return user.id