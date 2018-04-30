from peewee import *
from api.common.errors import NotFoundError
from playhouse.sqlite_ext import *
from engine.engine import notAlphaNumRegex
import datetime
import onb

class BaseModel(Model):
	created_date = DateTimeField(default=datetime.datetime.now)
	updated_date = DateTimeField(default=datetime.datetime.now)
	searchTable = None

	def save(self, *p, **pn):
		self.updated_date = datetime.datetime.now()
		super().save(*p, **pn)

	def updateFrom(self, vals, autoSave=True):
		for key, val in vals.items():
			if isinstance(getattr(self, key), BaseModel):
				getattr(self, key).updateFrom(val, autoSave=autoSave)
			else:
				setattr(self, key, val)
		if autoSave:
			self.save()

	@classmethod
	def search(cls, phrase):
		""" Search phrase will be converted to lowercase letters and nums prefixs"""
		if not cls.searchTable:
			raise Exception('search table not implemented for this table')

		phrase = notAlphaNumRegex.sub('', phrase).lower().split()
		phrase = " OR ".join([word + '*' for word in phrase]) or '*'

		return (cls.select().join(
				cls.searchTable,
				on=(cls.id == cls.searchTable.rowid))
			.where(cls.searchTable.match(phrase))
			.order_by(cls.searchTable.bm25()))

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

FTSenabledModel = FTS5Model if FTS5Model.fts5_installed() else FTSModel