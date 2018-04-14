from ..sqldbmodel import SqldbTestModel
from sqldb.models.basemodels import *
from sqldb.models.user import *
from engine.engine import Rand
import peewee, datetime

class UserModelTest(SqldbTestModel):
	def setUp(self):
		super().setUp()
		self.user = User.create(username=Rand.randomString())

	def test_create(self):
		self.assertNotEqual(self.user.created_date, None)
		self.assertNotEqual(self.user.updated_date, None)

	def test_createSameName(self):
		with self.assertRaises(peewee.IntegrityError):
			user2 = User.create(username=self.user.username)

	def test_save(self):
		t = datetime.datetime.now()
		self.user.save()
		self.assertTrue(self.user.created_date < t < self.user.updated_date)

	def test_delete(self):
		userid = self.user.id
		self.user.delete_instance()
		self.assertFalse(User.select().where(User.id == userid).exists())