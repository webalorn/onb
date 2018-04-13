from flask_restful import fields
import flask_jwt_extended as fjwt
import copy

"""class AuthTokenField(fields.Raw):
	def format(self, value):
		return "Urgent" if value & 0x01 else "Normal"""

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
}

auth_user_fields = {
	**copy.deepcopy(user_fields),
	"auth_token": fields.String(attribute=lambda user: fjwt.create_access_token(identity=user)),
}