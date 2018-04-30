from flask_restful import fields
import flask_jwt_extended as fjwt
from .common_fields import MarshalFields

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'is_admin': fields.Boolean,
	'is_anonymous': fields.Boolean(attribute=lambda user: user.isAnonymous()),
	'profile': MarshalFields({
		'avatar_id': fields.Integer,
		'description': fields.String,
		'birthdate': fields.DateTime,
		'country': fields.String,
		'gender': fields.String,
		'first_name': fields.String,
		'last_name': fields.String,
	}),
	'settings': MarshalFields({
		'language': fields.String,
		'i12n_editor': fields.Boolean,
	}),
}

auth_user_fields = {
	**user_fields,
	"auth_token": fields.String(attribute=lambda user: fjwt.create_access_token(identity=user)),
}