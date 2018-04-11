from .enginetestmodel import EngineTestModel
from engine.engine import *

class SingletonClassTest(EngineTestModel):
	def test_is_singleton(self):
		class SingletonTest(metaclass=Singleton):
			pass
		self.assertIs(SingletonTest(), SingletonTest())

class RandClassTest(EngineTestModel):
	def test_random(self):
		self.assertNotEqual(Rand.randomString(20), Rand.randomString(20))

	def test_defaultSize(self):
		self.assertTrue(len(Rand.randomString()) == 10)

	def test_size(self):
		self.assertTrue(len(Rand.randomString(2)) == 2)

	def test_sizeZero(self):
		self.assertTrue(len(Rand.randomString(0)) == 0)

	def test_rollRange(self):
		for roll in range(100):
			self.assertIn(Rand.roll(3), [1, 2, 3])

class MapClassTest(EngineTestModel):
	def test_simpleAccess(self):
		m = Map({'a':'a_value'})
		self.assertEqual(m.a, 'a_value')

	def test_recursiveAccess(self):
		m = Map({'foo':{'bar':{'a':12}}})
		self.assertEqual(m.foo.bar.a, 12)

	def test_recursiveAccessBrackets(self):
		m = Map({'foo':{'bar':{'a':12}}})
		self.assertEqual(m['foo'].bar.a, 12)