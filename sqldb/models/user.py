from peewee import *
from .basemodels import *
from .customfields import *
import bcrypt

"""class UserIndex(IndexModel, SqlTableModel):
	username = SearchField()"""

class UserProfile(BaseModel, SqlTableModel):
	avatar_id = IntegerField(null=True, default=None)
	description = TextField(default="")
	birthdate = DateTimeField(null=True, default=None)
	country = TextField(null=True, default=None)
	gender = CharField(null=True, default=None)
	first_name = TextField(default="")
	last_name = TextField(default="")

class UserSettings(BaseModel, SqlTableModel):
	language = TextField(default='en')
	i18n_editor = BooleanField(default=False)

class User(BaseModel, SqlTableModel):
	username = CharField(unique=True, null=True)
	password_hash = TextField(null=True)
	is_admin = BooleanField(default=False)
	jwt_revoked_at = IntegerField(default=0)

	battles = PyDataField(default=[]) # List of ids

	friends = PyDataField(default=[])
	followers = PyDataField(default=[])

	profile = ForeignKeyField(UserProfile, on_delete='CASCADE')
	settings = ForeignKeyField(UserSettings, on_delete='CASCADE')

	def save(self, *p, **pn):
		super().save(*p, **pn)

	#searchTable = UserIndex

	def isAnonymous(self):
		return self.username == None

	def getFriends(self):
		return list(User.select().where(User.id << self.friends))

	def getFollowers(self):
		return list(User.select().where(User.id << self.followers))

	def addFriend(self, friend_id):
		if not friend_id in self.friends and self.id != friend_id:
			self.friends.append(friend_id)
			self.save()

			friend = User.get(id=friend_id)
			if not self.id in friend.followers:
				friend.followers.append(friend_id)
				friend.save()

	def removeFriend(self, friend_id):
		if friend_id in self.friends:
			self.friends.remove(friend_id)
			self.save()

		friend = User.get(id=friend_id)
		if self.id in friend.followers:
			friend.followers.remove(friend_id)
			friend.save()


	# Auth methods

	def verifyPassword(self, password):
		return bcrypt.checkpw(password.encode('utf8'), self.password_hash.encode('utf8'))

	def setPassword(self, password):
		self.password_hash = self.hashPassword(password)

	def revoke_all_jwt(self):
		self.jwt_revoked_at += 1
		self.save()


	# Battles

	def add_battle(self, battle_id):
		if not battle_id in self.battles:
			self.battles.append(battle_id)

	def remove_battle(self, battle_id):
		if battle_id in self.battles:
			self.battles.remove(battle_id)

	def getBattles(self):
		from .battle import Battle
		return Battle.select().where(Battle.id << self.battles)

	# Static methods

	@classmethod
	def usernameExists(cls, username):
		return bool(cls.select().where(cls.username == username))

	@classmethod
	def create(cls, *p, **pn):
		return super().create(*p, **pn,
			profile_id=UserProfile.create().id,
			settings_id=UserSettings.create().id,
		)

	@classmethod
	def hashPassword(cls, password):
		salt = bcrypt.gensalt()
		password = password.encode('utf8')
		return bcrypt.hashpw(password, salt)

class OwnedObject(BaseModel): # Every user can read, only the owner can write
	owner = ForeignKeyField(User, null=True, default=None, on_delete='CASCADE')
	is_official = BooleanField(default=False) # If true, marked as official content
	is_public = BooleanField(default=True) # If true, marked as official content
	is_generated = BooleanField(default=False) # If true, the owner can't modify this object directly