from flask_restful import fields
import flask_jwt_extended as fjwt
import copy

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
}

auth_user_fields = {
	**copy.deepcopy(user_fields),
	"auth_token": fields.String(attribute=lambda user: fjwt.create_access_token(identity=user)),
}