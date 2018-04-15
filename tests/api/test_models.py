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
