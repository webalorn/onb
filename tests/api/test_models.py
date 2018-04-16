from .apitestmodel import ApiTestModel
from api.common.errors import *

class ApiModelTest(ApiTestModel):
	def test_getModelList(self):
		data = self.app_get('/model/unit', 200, data={})
		self.assertInJson([{
			"id": 1,
			"owner_id": 1,
			"type": "unit",
			"is_official": self.AnyValue,
			"is_public": True,
			"is_generated": False,
			"model": {"name": "unit1", "description": "space gobelin", 'summary': self.AnyValue, 'race': self.AnyValue}
		}], data)
		self.assertNotInJson([{'is_public': False}], data)
		self.assertNotInJson([{'model':{'categories':self.AnyValue}}], data)
		self.assertTrue(len(data) >= 5)

		token = self.getUserToken('test_user', '1234')
		data = self.app_get('/model/unit', 200, data={}, token=token)
		self.assertInJson([self.AnyValue]*5 + [{'is_public': False}], data)

		# Pages
		data = self.app_get('/model/unit', 200, data={'pagination': 2})
		self.assertEqual(len(data), 2)

		data = self.app_get('/model/unit/page/1', 200, data={'pagination': 2})
		self.assertEqual(len(data), 2)
		self.assertInJson([{'id':1}], data)
		self.assertNotInJson([{'id':3}], data)

		data = self.app_get('/model/unit/page/2', 200, data={'pagination': 2})
		self.assertEqual(len(data), 2)
		self.assertInJson([{'id':3}], data)
		self.assertNotInJson([{'id':1}], data)

		# Filters
		data = self.app_get('/model/unit', 200, data={'only_official': True})
		self.assertInJson([{'is_official': True}], data)
		self.assertNotInJson([{'is_official': False}], data)

	def test_searchModel(self):
		data = self.app_get("/model/unit/search", 200, data={'search': 'gob'})
		self.assertInJson([{'id':3}, {'id': 1}, {'id':2}, {'id': 4}], data)
		self.assertEqual(len(data), 4)

		data = self.app_get("/model/unit/search", 200, data={'search': 'gob', 'only_official':True})
		self.assertInJson([{'id': 3}, {'id': 4}], data)
		self.assertEqual(len(data), 2)

	def test_getModel(self):
		self.assertInJson({"id": 5, "owner_id": 1, "is_official": True, 'schema': None},
			self.app_get("/model/unit/5", 200))
		self.assertInJson({"id": 5, 'schema': {"type": "model", "model_name": "unit"}},
			self.app_get("/model/unit/5", 200, data={'schema': True}))
		
		with self.assertRaises(NotFoundError):
			self.app_get("/model/unit/2000", 500)
		
		with self.assertRaises(NotFoundError):
			self.app_get("/model/unit/6", 500)

		token = self.getUserToken('test_user', '1234')
		self.assertInJson({"id": 6, "owner_id": 1, "is_public": False,
				'model': {'movement': {'duration': self.AnyValue}}, 'schema': None},
			self.app_get("/model/unit/6", 200, token=token))

	def createModelGetId(self, data={}):
		token = self.getUserToken('test_user', '1234')
		return self.app_post('/model/unit', 200, data=data, token=token)['id']

	def test_createModel(self):
		self.app_post('/model/unit', 401, data={'name': 'Troll'})

		token = self.getUserToken('test_user', '1234')
		data1 = self.app_post('/model/unit', 200, data={'name': 'Troll'}, token=token)

		self.assertInJson({"id": self.AnyValue, "owner_id": 1, 'is_official': False, "is_public": True,
			'model': {'movement': {'duration': self.AnyValue}, 'name': 'Troll'},
			'schema': None}, data1)

		data2 = self.app_post('/model/unit', 200, data={'name': 'Troll'}, token=token)
		self.assertEqual(data1['id']+1, data2['id'])
		