from flask_restful import reqparse, inputs

class FakeRequest(dict):
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

class ExtendedParser(reqparse.RequestParser):
	def add_argument(self, *p, **pn):
		pn['location'] = 'json'
		if not 'store_missing' in pn and not 'default' in pn:
			pn['store_missing'] = False
		super().add_argument(*p, **pn)

	def parse_args_from(self, vals):
		fake_request = FakeRequest()
		setattr(fake_request, 'json', vals)
		setattr(fake_request, 'unparsed_arguments', {})
		return self.parse_args(fake_request)