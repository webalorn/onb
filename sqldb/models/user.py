from peewee import *
from .basemodels import BaseModel, SqlTableModel
import bcrypt

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
	i12n_editor = BooleanField(default=False)

class User(BaseModel, SqlTableModel):
	username = CharField(unique=True, null=True)
	password_hash = TextField(null=True)
	is_admin = BooleanField(default=False)
	jwt_revoked_at = IntegerField(default=0)

	profile = ForeignKeyField(UserProfile)
	settings = ForeignKeyField(UserSettings)

	def isAnonymous(self):
		return self.username == None

	def save(self, *p, **pn):
		super().save(*p, **pn)

	def verifyPassword(self, password):
		return bcrypt.checkpw(password.encode('utf8'), self.password_hash.encode('utf8'))

	def setPassword(self, password):
		self.password_hash = self.hashPassword(password)

	def revoke_all_jwt(self):
		self.jwt_revoked_at += 1
		self.save()

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
	owner = ForeignKeyField(User, null=True, default=None)
	is_official = BooleanField(default=False) # If true, marked as official content
	is_public = BooleanField(default=True) # If true, marked as official content
	is_generated = BooleanField(default=False) # If true, the owner can't modify this object directly