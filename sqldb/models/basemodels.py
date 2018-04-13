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