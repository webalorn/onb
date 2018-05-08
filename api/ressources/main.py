from flask_restful import Resource, marshal_with
from api.fields.main import config_fields
import onb, yaml, os

@onb.api.resource('/')
class ApiReference(Resource):
	def get(self):
		filename = os.path.join(onb.OnbSettings.root, 'api/swagger_doc.yml')

		with open(filename, 'r') as f:
			return yaml.load(f)

@onb.api.resource('/config')
class ApiConfig(Resource):
	@marshal_with(config_fields)
	def get(self):
		return onb.conf