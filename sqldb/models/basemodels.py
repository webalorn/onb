from peewee import *
import datetime
import onb

class BaseModel(Model):
	class Meta:
		database = onb.sqldb

class TableModel(Model): # Every model that inherit from this model will be added as a database table
	pass

# User models

class User(BaseModel, TableModel):
	username = CharField(unique=True)
	def save(self, *p, **pn):
		print("Sauvegarder")
		super().save(*p, **pn)

class OwnedObject(BaseModel):
	owner = ForeignKeyField(User)
	is_public = BooleanField(default=False) # If true, other users can read, but not write

# Values objects

class Value(OwnedObject, TableModel):
	""" Values are the values a field can take """
	value = TextField()
	field_name = TextField()
	description = TextField(default="")