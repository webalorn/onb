from flask_restful import fields, marshal

class MarshalFields(fields.Raw):
	def format(self, value):
		return marshal(value, self.datas)

	def __init__(self, datas, *p, **pn):
		self.datas = datas
		return super().__init__(*p, **pn)

class DayDate(fields.Raw):
	def format(self, value):
		return value.strftime("%d-%m-%Y")

class AnyFields(fields.Raw):
	""" Use only when it's sure that the value already have the correct format """
	def format(self, value):
		return value