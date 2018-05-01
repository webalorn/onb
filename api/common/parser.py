from flask_restful import reqparse, inputs
from api.common.errors import *

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

def checkPagination(pagination, maxi=100):
	if (pagination < 1):
		raise BadRequestError('pagination value must be at least 1')
	if (pagination > maxi):
		raise BadRequestError('pagination value must be at most ' + str(maxi))
