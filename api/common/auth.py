import onb
from sqldb.models.user import User as sqlUser

@onb.jwt.user_identity_loader
def user_identity_lookup(user):
	return user.id

@onb.jwt.user_loader_callback_loader
def user_loader_callback(identity):
	try:
		return sqlUser.get(id=identity)
	except:
		return None