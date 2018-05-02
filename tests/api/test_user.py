from .apitestmodel import ApiTestModel
from api.common.errors import *

class ApiUserTest(ApiTestModel):
	def test_getUser(self):
		data = self.app_get('/user/1', 200)
		self.assertInJson({'id': 1, 'username': 'test_user', 'is_anonymous': False,
			'profile': self.AnyValue, 'friends': self.AnyValue, 'followers': self.AnyValue}, data)
		self.assertNotInJson({'auth_token': self.AnyValue, 'settings':self.AnyValue}, data)

		self.app_get('/user', 401)

		token = self.getUserToken('test_user', '1234')
		profileData = self.app_get('/user', 200, token=token)
		self.assertInJson({'id': 1, 'auth_token': self.AnyValue,
			'profile': self.AnyValue, 'settings': self.AnyValue},
		profileData)


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
		userDatas = self.app_get('/user/anonymous', 200, data={})
		self.assertInJson({'id':self.AnyValue, 'username': None, 'auth_token': self.AnyValue, 'is_anonymous': True}, userDatas)
		token = userDatas['auth_token']

		# Claim account
		self.assertInJson(
			{"msg": "Missing Authorization Header"},
			self.app_post('/user/anonymous', 401, data={})
		)
		self.app_post('/user/anonymous', 422, data={}, token="")
		self.app_post('/user/anonymous', 422, data={}, token="1234")
		
		self.assertInJson(
			{"message": {'username': self.AnyValue}},
			self.app_post('/user/anonymous', 400, data={}, token=token)
		)
		with self.assertRaises(UserAlreadyExistsError):
			claimDatas = self.app_post("/user/anonymous", 500, data={'username': 'test_user', 'password': 1234}, token=token)

		username = self.newUsername()
		self.assertInJson(
			{"username": username, "auth_token": self.AnyValue, 'is_anonymous': False},
			self.app_post('/user/anonymous', 200, data={'username': username, 'password': 1234}, token=token)
		)
		with self.assertRaises(NotFoundError):
			claimDatas = self.app_post("/user/anonymous", 500, data={'username': username, 'password': 1234}, token=token)

	def test_updateUser(self):
		username = self.newUsername()
		user_id = self.createUser(username, '1234')
		token = self.getUserToken(username, '1234')

		datas = self.app_put('/user', 200, data={
			"username": "gob36",
			"password": "newpass",
			"profile": {
				"avatar_id": 12,
				"description": "I'm a gobalin warrior !",
				"birthdate": "10-03-1940",
				"country": "France",
				"gender": "M",
				"first_name": "Mr Goblin",
				"last_name": "WRRGR !",
				"foo": "bar",
			},
			"settings": {
				"language": "fr",
				"i18n_editor": True,
				"foo": "bar",
			}
		}, token=token)
		self.assertInJson({
			"profile": {
				"avatar_id": 12,
				"description": "I'm a gobalin warrior !",
				"birthdate": "10-03-1940",
				"country": "France",
				"gender": "M",
				"first_name": "Mr Goblin",
				"last_name": "WRRGR !",
			},
			"settings": {
				"language": "fr",
				"i18n_editor": True,
			}
		}, datas)
		self.assertNotInJson({
			"username": "gob36",
			"profile": {
				"foo": "bar",
			},
			"settings": {
				"foo": "bar",
			}
		}, datas);
		with self.assertRaises(UserAuthError):
			self.app_get('/user/auth', 400, data={'username': username, 'password': "newpass"})

		self.app_put('/user', 400, data={"settings": {"language": "es"}}, token=token)

		self.app_put('/user', 200, data={"profile": {"gender": None}}, token=token)
		self.app_put('/user', 200, data={"profile": {"gender": "M"}}, token=token)
		self.app_put('/user', 200, data={"profile": {"gender": "F"}}, token=token)
		self.app_put('/user', 400, data={"profile": {"gender": "A"}}, token=token)

		self.app_put('/user', 400, data={"profile": {"birthdate": "13 March 1990"}}, token=token)

	def test_getUsernameAvailability(self):
		datas = self.app_get('/user/username_available', 200, data=self.newUsername())
		self.assertInJson({'available': True}, datas)

		datas = self.app_get('/user/username_available', 409, data='test_user')
		self.assertInJson({'available': False, 'suggestions': self.AnyValue}, datas)
		self.assertEqual(len(datas['suggestions']), 5)

	def test_logout(self):
		username = self.newUsername()
		self.createUser(username, '12345')
		token = self.getUserToken(username, '12345')

		self.app_get('/user', 200, token=token)
		self.app_delete('/user/auth', 200, token=token)
		self.app_get('/user', 401, token=token)

		token = self.getUserToken(username, '12345')
		self.app_get('/user', 200, token=token)

	def test_newPassword(self):
		username = self.newUsername()
		self.createUser(username, '12345')
		token = self.getUserToken(username, '12345')

		with self.assertRaises(UserAuthError):
			self.app_post('/user/auth', 400, data={'password': '', 'new_password': "newpass"}, token=token)

		self.app_post('/user/auth', 200, data={'password': '12345', 'new_password': "newpass"}, token=token)

		with self.assertRaises(UserAuthError):
			self.app_get('/user/auth', 400, data={'username': username, 'password': "12345"})
		self.app_get('/user/auth', 200, data={'username': username, 'password': "newpass"})

	"""def test_searchUser(self):
		datas = self.app_get('/user/search', 200, data={"search": "user"})
		self.assertTrue(len(datas) >= 1)
		self.assertInJson([{'id': self.AnyValue, 'username': self.AnyValue}], datas);
		self.assertNotInJson([{'firends': self.AnyValue, 'followers': self.AnyValue}], datas)

		datas = self.app_get('/user/search', 200, data={"search": self.newUsername()})
		self.assertEqual(len(datas), 0)"""

	def test_friends(self):
		users = []
		for i in range(5):
			username = self.newUsername()
			user_id = self.createUser(username, '1234')
			token = self.getUserToken(username, '1234')
			users.append({'username': username, 'id': user_id, 'token': token})

		with self.assertRaises(NotFoundError):
			self.app_post('/user/friend/'+ str(users[0]['id']), 404, token=users[0]['token'])

		for i in range(1, 5):
			self.app_post('/user/friend/' + str(users[i]['id']), 200, token=users[0]['token'])

		datas = self.app_get('/user', 200, token=users[0]['token'])
		self.assertEqual(len(datas['friends']), 4)
		self.assertEqual(len(datas['followers']), 0)

		for i in range(1, 5):
			datas = self.app_get('/user', 200, token=users[i]['token'])
			self.assertEqual(len(datas['friends']), 0)
			self.assertEqual(len(datas['followers']), 1)
			self.assertInJson({'followers': [{'id': users[0]['id']}]}, datas)

		self.app_delete('/user/friend/' + str(users[1]['id']), 200, token=users[0]['token'])
		self.app_delete('/user/friend/' + str(users[1]['id']), 200, token=users[0]['token'])

		datas = self.app_get('/user', 200, token=users[0]['token'])
		self.assertEqual(len(datas['friends']), 3)

		datas = self.app_get('/user', 200, token=users[1]['token'])
		self.assertEqual(len(datas['followers']), 0)