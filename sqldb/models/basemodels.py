from peewee import *
import datetime
import onb

class BaseModel(Model):
	class Meta:
		database = onb.sqldb

class TableModel(Model): # Every mol that inherit from this model will be added as a database table
	pass

# User models

class User(BaseModel, TableModel):
	username = CharField(unique=True)
	def save(self, *p, **pn):
		print("Sauvegarder")
		super().save(*p, **pn)

class OwnedObject(BaseModel):
	user = ForeignKeyField(User)