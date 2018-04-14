from .apitestmodel import ApiTestModel
from sqldb.models.user import User
from api.common.errors import *
import random

class ApiUserTest(ApiTestModel):
	def createUser(self, username, password=None):
		if password:
			password = User.hashPassword(password)
		return User.create(username=username, password_hash=password).id

	def authUser(self, username, password):
		return self.app_get('/user/auth', 200, data={'username': username, 'password': password})['auth_token']

	def test_getUserList(self):
		data = self.app_get('/user/1', 200)
		self.assertInJson({'id': 1, 'username': 'test_user', 'is_anonymous': False}, data)
		self.assertNotInJson({'auth_token': self.AnyValue}, data)

	def test_auth(self):
		self.assertInJson(
			{"message": {'username': self.AnyValue}},
			self.app_get('/user/auth', 400, data={})
		)
		with self.assertRaises(UserAuthError):
			self.app_get('/user/auth', 400, data={'username': 'test_user', 'password': 123})

		self.assertInJson(
			{"username": "test_user", "auth_token": self.AnyValue},
			self.app_get('/user/auth', 200, data={'username': 'test_user', 'password': 1234})
		)