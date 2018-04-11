from ..enginetestmodel import EngineTestModel
from engine.datas.fieldvalues import *
from engine.models.gameentities import UnitModel
import random

class IntFieldTest(EngineTestModel):
	def setUp(self):
		self.field = IntField()

	def test_allowedValues(self):
		self.assertEqual(self.field.castFunction(0), 0)
		self.assertEqual(self.field.castFunction(1), 1)
		for k in [random.randint(-1000, 1000) for _ in range(10)]:
			self.assertEqual(self.field.castFunction(k), k)
		self.assertEqual(self.field.castFunction(12.2), 12)
		self.assertEqual(self.field.castFunction(12.9), 12)

	def test_notAllowedValues(self):
		self.assertEqual(self.field.castFunction(None), 0)
		self.assertEqual(self.field.castFunction("str"), 0)

	def test_optional(self):
		self.field = IntField(optional=True)
		self.assertEqual(self.field.castFunction(None), None)
		self.assertEqual(self.field.castFunction(12), 12)

	def test_defaultValue(self):
		self.field = IntField(12)
		self.assertEqual(self.field.defaultValue(), 12)

		self.field = IntField(default=12)
		self.assertEqual(self.field.defaultValue(), 12)

		self.field = IntField(default=None)
		self.assertEqual(self.field.defaultValue(), 0)

		self.field = IntField(default="str")
		self.assertEqual(self.field.defaultValue(), 0)

	def test_getDbValue(self):
		self.assertIs(self.field.getDbValue(11), 11)

	def test_setUnderMax(self):
		self.field = IntField(max=10)
		self.assertEqual(self.field.setUnderMax(12), 10)
		self.assertEqual(self.field.setUnderMax(8), 8)
		self.assertEqual(self.field.setUnderMax(-20), -20)

	def test_setAboveMin(self):
		self.field = IntField(min=10)
		self.assertEqual(self.field.setAboveMin(12), 12)
		self.assertEqual(self.field.setAboveMin(8), 10)
		self.assertEqual(self.field.setAboveMin(-20), 10)

	def test_setInValidValues(self):
		self.field = IntField(values=[12, 14, 20])
		self.assertEqual(self.field.setInValidValues(14), 14)
		self.assertEqual(self.field.setInValidValues(8), 12)
		self.assertEqual(self.field.setInValidValues(-20), 12)

		self.field = IntField(values=[])
		self.assertEqual(self.field.setInValidValues(8), 8)

	def test_creatValue(self):
		self.assertEqual(self.field.createValue(), 0)

	def test_getType(self):
		self.assertEqual(self.field.getTypeRep(), 'int')

	def test_type(self):
		self.assertEqual(self.field.type(), int)

class BoolFieldTest(EngineTestModel):
	def setUp(self):
		self.field = BoolField()

	def test_allowedValues(self):
		self.assertEqual(self.field.castFunction(0), False)
		self.assertEqual(self.field.castFunction(1), True)
		self.assertEqual(self.field.castFunction(True), True)
		self.assertEqual(self.field.castFunction(12.2), True)
		self.assertEqual(self.field.castFunction(None), False)
		self.assertEqual(self.field.castFunction("str"), True)

	def test_getType(self):
		self.assertEqual(self.field.getTypeRep(), 'bool')

	def test_type(self):
		self.assertEqual(self.field.type(), bool)

class FloatFieldTest(EngineTestModel):
	def setUp(self):
		self.field = FloatField()

	def test_allowedValues(self):
		self.assertEqual(self.field.castFunction(0), 0.)
		self.assertEqual(self.field.castFunction(10.101), 10.101)
		self.assertEqual(self.field.castFunction(12.2), 12.2)
		self.assertEqual(self.field.castFunction(12.9), 12.9)

	def test_notAllowedValues(self):
		self.assertEqual(self.field.castFunction(None), 0.)
		self.assertEqual(self.field.castFunction("str"), 0.)

	def test_getType(self):
		self.assertEqual(self.field.getTypeRep(), 'float')

	def test_type(self):
		self.assertEqual(self.field.type(), float)

class PercentFieldTest(EngineTestModel):
	def setUp(self):
		self.field = PercentField()

	def test_allowedValues(self):
		self.assertEqual(self.field.castFunction(0), 0)
		self.assertEqual(self.field.castFunction(800), 800)
		self.assertEqual(self.field.castFunction(-102.2),  -102)

	def test_defaultValue(self):
		self.assertEqual(self.field.defaultValue(), 100)

	def test_getType(self):
		self.assertEqual(self.field.getTypeRep(), 'percent')

	def test_type(self):
		self.assertEqual(self.field.type(), int)

class StringFieldTest(EngineTestModel):
	def setUp(self):
		self.field = StringField()

	def test_allowedValues(self):
		self.assertEqual(self.field.castFunction("foo"), "foo")
		self.assertEqual(self.field.castFunction(1), '1')
		self.assertEqual(self.field.castFunction(True), 'True')
		self.assertEqual(self.field.castFunction(False), 'False')
		self.assertEqual(self.field.castFunction(12.2), '12.2')
		self.assertEqual(self.field.castFunction(None), '')
		self.assertEqual(self.field.castFunction("str"), 'str')

	def test_setUnderMax(self):
		self.field = StringField(max=4)
		self.assertEqual(self.field.setUnderMax("foo"), "foo")
		self.assertEqual(self.field.setUnderMax("foo_bar"), "foo_")

	def test_setAboveMin(self):
		self.field = StringField(min=6)
		self.assertEqual(self.field.setAboveMin("foo_bar"), "foo_bar")
		self.assertEqual(self.field.setAboveMin("foo"), "foo   ")

	def test_getType(self):
		self.assertEqual(self.field.getTypeRep(), 'string')

	def test_type(self):
		self.assertEqual(self.field.type(), str)

class ClassFieldTest(EngineTestModel):
	def setUp(self):
		self.field = ClassField('unit')

	def test_createValue(self):
		self.assertIsInstance(self.field.createValue(), UnitModel)
		self.field = ClassField('unit', [{'name':'Conan'}])
		self.assertEqual(self.field.createValue().name, 'Conan')

	def test_getType(self):
		self.assertEqual(self.field.getTypeRep(), 'class')

	def test_type(self):
		self.assertEqual(self.field.type(), UnitModel)