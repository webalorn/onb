from ..sqldb.sqldbmodel import SqldbTestModel
import api.api, onb, json
from engine.engine import Rand
from werkzeug.wrappers import Headers

class ApiTestModel(SqldbTestModel):
	def setUp(self):
		super().setUp()
		self.app = onb.app.test_client()

	### Restfull requests

	def checkContentType(self, headers):
		self.assertEqual(headers['Content-Type'], 'application/json')

	def makeAppRequest(self, endpoint, method, checkCode, **kw):
		headers = kw['headers'] if 'headers' in kw else Headers()
		if 'token' in kw:
			headers.add('Authorization', "Bearer " + kw['token'])
			del kw['token']
		kw['headers'] = headers

		request = getattr(self.app, method)(endpoint, **kw)
		self.checkContentType(request.headers)
		self.assertEqual(request.status_code, checkCode)
		return json.loads(request.data)

	def app_get(self, endpoint, checkCode, **kw):
		return self.makeAppRequest(endpoint, 'get', checkCode, **kw)

	def app_post(self, endpoint, checkCode, **kw):
		return self.makeAppRequest(endpoint, 'post', checkCode, **kw)

	def app_put(self, endpoint, checkCode, **kw):
		return self.makeAppRequest(endpoint, 'put', checkCode, **kw)

	def app_delete(self, endpoint, checkCode, **kw):
		return self.makeAppRequest(endpoint, 'delete', checkCode, **kw)

	### User utils functions


	def createUser(self, username, password=None):
		if password:
			password = User.hashPassword(password)
		return User.create(username=username, password_hash=password).id

	def createAnonymous(self):
		return User.create().id

	def newUsername(self):
		return Rand.randomString()

	def getUserToken(self, username, password):
		return self.app_get('/user/auth', 200, data={'username': username, 'password': password})['auth_token']

	### Assert functions

	class AnyValue:
		""" Used to validate any value in json schema """
		pass

	def assertInJson(self, schema, data):
		if isinstance(schema, dict):
			self.assertIsInstance(data, dict)
			for key in schema:
				self.assertIn(key, data)
				self.assertInJson(schema[key], data[key])
		elif isinstance(schema, list):
			self.assertIsInstance(data, list)
			self.assertTrue(len(schema) <= len(data))
			for i in range(len(schema)):
				self.assertInJson(schema[i], data[i])
		elif schema != self.AnyValue:
			self.assertEqual(schema, data)

	def assertNotContainedInJson(self, schema, data):
		""" Raise an error if all the schema is contained in 'data' """
		try:
			self.assertInJson(schema, data)
		except AssertionError:
			return 
		raise AssertionError

	def assertNotInJson(self, schema, data):
		""" Raise an error if any value in 'schema' is found in 'data' """
		if isinstance(schema, dict) and isinstance(data, dict):
			for key in schema:
				if key in data:
					self.assertNotInJson(schema[key], data[key])
		elif isinstance(schema, list) and isinstance(data, list):
			for i in range(min(len(schema), len(data))):
				self.assertNotInJson(schema[i], data[i])
		else:
			self.assertNotEqual(schema, data)
			self.assertNotEqual(schema, self.AnyValue)