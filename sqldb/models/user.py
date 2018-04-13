from peewee import *
from .basemodels import BaseModel, TableModel
import bcrypt

class User(BaseModel, TableModel):
	username = CharField(unique=True, null=True)
	password_hash = TextField(null=True)

	def isAnonymous(self):
		return self.username == None

	def save(self, *p, **pn):
		super().save(*p, **pn)

	@classmethod
	def hashPassword(cls, password):
		salt = bcrypt.gensalt()
		password = password.encode('utf8')
		return bcrypt.hashpw(password, salt)

	def verifyPassword(self, password):
		return bcrypt.checkpw(password.encode('utf8'), self.password_hash.encode('utf8'))

	def setPassword(self, password):
		self.password_hash = self.hashPassword(password)

class OwnedObject(BaseModel): # Every user can read, only the owner can write
	owner = ForeignKeyField(User, null=True, default=None)
	is_official = BooleanField(default=False) # If true, marked as official content
	is_public = BooleanField(default=True) # If true, marked as official content
	is_generated = BooleanField(default=False) # If true, the owner can't modify this object directly