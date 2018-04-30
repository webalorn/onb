from flask_restful import fields, marshal

class MarshalFields(fields.Raw):
	def format(self, value):
		return marshal(value, self.datas)

	def __init__(self, datas, *p, **pn):
		self.datas = datas
		return super().__init__(*p, **pn)