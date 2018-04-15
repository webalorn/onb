from .apitestmodel import ApiTestModel
from sqldb.models.user import User
from api.common.errors import *
import random

class ApiUserTest(ApiTestModel):
	def test_getUser(self):
		data = self.app_get('/user/1', 200)
		self.assertInJson({'id': 1, 'username': 'test_user', 'is_anonymous': False}, data)
		self.assertNotInJson({'auth_token': self.AnyValue}, data)

		self.app_get('/user', 401)

		token = self.getUserToken('test_user', '1234')
		profileData = self.app_get('/user', 200, token=token)
		self.assertInJson({'id': 1, 'auth_token': self.AnyValue}, profileData)


		self.assertEqual(self.app_get('/user/1', 200, token=token), data)

	def test_auth(self):
		# Test auth endpoint
		self.assertInJson(
			{"message": {'username': self.AnyValue}},
			self.app_get('/user/auth', 400, data={})
		)
		with self.assertRaises(UserAuthError):
			self.app_get('/user/auth', 400, data={'username': 'not_an_user', 'password': 1234})
		with self.assertRaises(UserAuthError):
			self.app_get('/user/auth', 400, data={'username': 'test_user', 'password': 123})

		self.assertInJson(
			{"username": "test_user", "auth_token": self.AnyValue},
			self.app_get('/user/auth', 200, data={'username': 'test_user', 'password': 1234})
		)

	def test_createUser(self):
		self.assertInJson(
			{"message": {'username': self.AnyValue}},
			self.app_post('/user', 400, data={})
		)
		self.assertInJson(
			{"message": {'password': self.AnyValue}},
			self.app_post('/user', 400, data={'username': 'gobelin'})
		)
		with self.assertRaises(UserAlreadyExistsError):
			self.app_post('/user', 400, data={'username': 'test_user', 'password': 1234})
		
		username = self.newUsername()
		datas = self.app_post('/user', 200, data={'username': username, 'password': 1234})
		self.assertInJson({'id':self.AnyValue, 'username': username, 'auth_token': self.AnyValue, 'is_anonymous': False}, datas)

	def test_userAnonymous(self):
		userDatas = self.app_post('/user/anonymous', 200, data={})
		self.assertInJson({'id':self.AnyValue, 'username': None, 'auth_token': self.AnyValue, 'is_anonymous': True}, userDatas)
		token = userDatas['auth_token']

		# Claim account
		self.assertInJson(
			{"msg": "Missing Authorization Header"},
			self.app_put('/user/anonymous', 401, data={})
		)
		self.app_put('/user/anonymous', 422, data={}, token="")
		self.app_put('/user/anonymous', 422, data={}, token="1234")
		
		self.assertInJson(
			{"message": {'username': self.AnyValue}},
			self.app_put('/user/anonymous', 400, data={}, token=token)
		)
		with self.assertRaises(UserAlreadyExistsError):
			claimDatas = self.app_put("/user/anonymous", 500, data={'username': 'test_user', 'password': 1234}, token=token)

		username = self.newUsername()
		self.assertInJson(
			{"username": username, "auth_token": self.AnyValue, 'is_anonymous': False},
			self.app_put('/user/anonymous', 200, data={'username': username, 'password': 1234}, token=token)
		)
		with self.assertRaises(NotFoundError):
			claimDatas = self.app_put("/user/anonymous", 500, data={'username': username, 'password': 1234}, token=token)