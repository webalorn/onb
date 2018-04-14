from .apitestmodel import ApiTestModel

class ApiTestModelTest(ApiTestModel):
	### Test tool

	def test_assertInJson(self):
		self.assertInJson(1, 1)
		self.assertInJson({'id1':{'id2':{'id3':{'foo':1, 'bar':2}}}}, {'id1':{'id2':{'id3':{'foo':1, 'bar':2}}, 'other': 12}})
		self.assertInJson([1, 2, 3], [1, 2, 3, 4, 5])
		self.assertInJson([1, {'id': 12, 'foo': 'bar'}, 3], [1, {'my_id': 1, 'id': 12, 'foo': 'bar'}, 3, 4, 5])
		self.assertInJson({'id': self.AnyValue, 'foo': self.AnyValue}, {'my_id': 1, 'id': 12, 'foo': 'bar'})
		self.assertInJson([self.AnyValue, 2, 3], [1, 2, 3, 4, 5])
		self.assertInJson({'foo': self.AnyValue, 'bar': [self.AnyValue]}, {'foo': {'bar': 12}, 'bar': [[[12]]]})

		with self.assertRaises(AssertionError):
			self.assertInJson({'id': 12}, {})
		with self.assertRaises(AssertionError):
			self.assertInJson({'id': {'foo':'bar'}}, {'foo':'bar'})
		with self.assertRaises(AssertionError):
			self.assertInJson([1, 2, 3], [1, 2, 1, 3, 4, 5])
		with self.assertRaises(AssertionError):
			self.assertInJson([1, {'id': 12, 'foo': 'bar'}, 3], [1, 2, {'my_id': 12, 'foo': 'bar'}, 4, 5])
		with self.assertRaises(AssertionError):
			self.assertInJson({'id': self.AnyValue}, {})
		with self.assertRaises(AssertionError):
			self.assertInJson([self.AnyValue], [])
		with self.assertRaises(AssertionError):
			self.assertInJson([1, 2, 3], [self.AnyValue, 2, 3, 4, 5])

	def test_assertNotContainedInJson(self):
		with self.assertRaises(AssertionError):
			self.assertNotContainedInJson(1, 1)
		with self.assertRaises(AssertionError):
			self.assertNotContainedInJson({'id1':{'id2':{'id3':{'foo':1, 'bar':2}}}}, {'id1':{'id2':{'id3':{'foo':1, 'bar':2}}, 'other': 12}})
		with self.assertRaises(AssertionError):
			self.assertNotContainedInJson([1, 2, 3], [1, 2, 3, 4, 5])
		with self.assertRaises(AssertionError):
			self.assertNotContainedInJson([1, {'id': 12, 'foo': 'bar'}, 3], [1, {'my_id': 1, 'id': 12, 'foo': 'bar'}, 3, 4, 5])
		with self.assertRaises(AssertionError):
			self.assertNotContainedInJson({'id': self.AnyValue, 'foo': self.AnyValue}, {'my_id': 1, 'id': 12, 'foo': 'bar'})
		with self.assertRaises(AssertionError):
			self.assertNotContainedInJson([self.AnyValue, 2, 3], [1, 2, 3, 4, 5])
		with self.assertRaises(AssertionError):
			self.assertNotContainedInJson({'foo': self.AnyValue, 'bar': [self.AnyValue]}, {'foo': {'bar': 12}, 'bar': [[[12]]]})

		self.assertNotContainedInJson({'id': 12}, {})
		self.assertNotContainedInJson({'id': {'foo':'bar'}}, {'foo':'bar'})
		self.assertNotContainedInJson([1, 2, 3], [1, 2, 1, 3, 4, 5])
		self.assertNotContainedInJson([1, {'id': 12, 'foo': 'bar'}, 3], [1, 2, {'my_id': 12, 'foo': 'bar'}, 4, 5])
		self.assertNotContainedInJson({'id': self.AnyValue}, {})
		self.assertNotContainedInJson([self.AnyValue], [])
		self.assertNotContainedInJson([1, 2, 3], [self.AnyValue, 2, 3, 4, 5])

	def test_assertNotInJson(self):
		with self.assertRaises(AssertionError):
			self.assertNotInJson(1, 1)
		with self.assertRaises(AssertionError):
			self.assertNotInJson(self.AnyValue, {'a':1})
		with self.assertRaises(AssertionError):
			self.assertNotInJson({'id1':{'id2':{'id3':{'foo': 'bar'}}}}, {'id1':{'id2':{'id3':{'foo': 'bar'}}, 'other': 12}})
		with self.assertRaises(AssertionError):
			self.assertNotInJson([1, 2, 3], [1, 2, 3, 4, 5])
		with self.assertRaises(AssertionError):
			self.assertNotInJson({'foo': self.AnyValue}, {'foo': {'bar': 12}, 'bar': [[[12]]]})


		self.assertNotInJson([3, 1, 2, 3], [1, 2, 3, 4, 5])
		self.assertNotInJson({'token': self.AnyValue}, {'user': 'gobelin'})
		self.assertNotInJson({'user': {'gobelin':{}}}, {'user': {'gobelin':{}}})