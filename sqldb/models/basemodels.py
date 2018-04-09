from peewee import *
import datetime
import onb

class BaseModel(Model):
	created_date = DateTimeField(default=datetime.datetime.now)
	updated_date = DateTimeField(default=datetime.datetime.now)


	def save(self, *p, **pn):
		self.updated_date = datetime.datetime.now()
		super().save(*p, **pn)

	class Meta:
		database = onb.sqldb

class TableModel(Model): # Every model that inherit from this model will be added as a database table
	pass

# User models

class User(BaseModel, TableModel):
	username = CharField(unique=True)
	def save(self, *p, **pn):
		super().save(*p, **pn)

class OwnedObject(BaseModel): # Every user can read, only the owner can write
	owner = ForeignKeyField(User)
	is_official = BooleanField(default=False) # If true, marked as official content
	is_public = BooleanField(default=True) # If true, marked as official content
	is_generated = BooleanField(default=False) # If true, the owner can't modify this object directly

# Values objects

class Value(OwnedObject, TableModel):
	""" Values are the values a field can take """
	value = TextField()
	field_name = TextField()
	description = TextField(default="")