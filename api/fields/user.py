from flask_restful import fields
import flask_jwt_extended as fjwt

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
}

auth_user_fields = {
	**user_fields,
	"auth_token": fields.String(attribute=lambda user: fjwt.create_access_token(identity=user)),
}