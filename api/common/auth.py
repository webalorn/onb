import onb, datetime
from sqldb.models.user import User as sqlUser

@onb.jwt.user_identity_loader
def user_identity_lookup(user):
	return user.id

@onb.jwt.user_loader_callback_loader
def user_loader_callback(identity):
	try:
		user = sqlUser.get(id=identity)
		if datetime.datetime.now() - user.updated_date >= datetime.timedelta(hours=24):
			user.save()
		return user
	except:
		return None