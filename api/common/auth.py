import onb, datetime
import flask_jwt_extended as fjwt
from .errors import NotFoundError
from sqldb.models.user import User as sqlUser

@onb.jwt.user_identity_loader
def user_identity_lookup(user):
	return user.id

@onb.jwt.user_loader_callback_loader
def user_loader_callback(identity):
	try:
		user = sqlUser.get(id=identity)
		if datetime.datetime.now() - user.updated_date >= datetime.timedelta(hours=1):
			user.save()
		return user
	except:
		return None

def jwt_logged_user(fct, is_anonymous=False):
	def decoredFuntion(*p, **pn):
		if fjwt.get_current_user().isAnonymous() != is_anonymous:
			raise NotFoundError
		return fct(*p, **pn)
	return fjwt.jwt_required(decoredFuntion)

def jwt_anonymous_user(fct):
	return jwt_logged_user(fct, True)