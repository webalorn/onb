from peewee import *
from api.common.errors import NotFoundError
import datetime
import onb

class BaseModel(Model):
	created_date = DateTimeField(default=datetime.datetime.now)
	updated_date = DateTimeField(default=datetime.datetime.now)

	def save(self, *p, **pn):
		self.updated_date = datetime.datetime.now()
		super().save(*p, **pn)

	@classmethod
	def get(cls, *p, **pn):
		try:
			return super().get(*p, **pn)
		except DoesNotExist:
			raise NotFoundError

	class Meta:
		database = onb.sqldb

class SqlTableModel(): # Every model that inherit from this model will be added as a database table
	pass