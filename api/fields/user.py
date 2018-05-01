from flask_restful import fields, marshal
import flask_jwt_extended as fjwt
from sqldb.models.user import User as sqlUser
from .common_fields import MarshalFields, DayDate

short_profile = {
	'avatar_id': fields.Integer,
	'first_name': fields.String,
	'last_name': fields.String,
}

user_fields_short = {
	'id': fields.Integer,
	'username': fields.String,
	'is_admin': fields.Boolean,
	'is_anonymous': fields.Boolean(attribute=lambda user: user.isAnonymous()),
	'profile': MarshalFields(short_profile),
}

class FriendsField(fields.Raw):
	def format(self, friendList):
		return [marshal(val, user_fields_short) for val in friendList]

user_fields = {
	**user_fields_short,
	'is_anonymous': fields.Boolean(attribute=lambda user: user.isAnonymous()),
	'profile': MarshalFields({
		**short_profile,
		'description': fields.String,
		'birthdate': DayDate,
		'country': fields.String,
		'gender': fields.String,
	}),
	'friends': FriendsField(attribute=sqlUser.getFriends),
	'followers': FriendsField(attribute=sqlUser.getFollowers),
}

auth_user_fields = {
	**user_fields,
	"auth_token": fields.String(attribute=lambda user: fjwt.create_access_token(identity=user)),
	'settings': MarshalFields({
		'language': fields.String,
		'i12n_editor': fields.Boolean,
	}),
}