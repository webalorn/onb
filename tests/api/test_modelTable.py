from .apitestmodel import ApiTestModel
from api.common.errors import *

class ApiModelTableTest(ApiTestModel):
	def test_getTableModel(self):
		data = self.app_get('/model/table', 200)
		self.assertInJson({"model": {
			"first_line": self.AnyValue,
			"last_line": self.AnyValue,
			"pv_advance": [self.AnyValue],
			"by_lines_interval": [self.AnyValue],
			"table": [[self.AnyValue]],
			"_type": "game_table"}
		}, data)

		model = data['model']
		self.assertEqual(len(model['pv_advance']), len(model['by_lines_interval']))
		self.assertEqual(len(model['pv_advance']), len(model['table']))
		for k in range(len(model['table'])):
			self.assertEqual(len(model['table'][k]), model['last_line'] - model['first_line'] + 1)