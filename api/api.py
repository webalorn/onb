from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from api.common.errors import errors
import onb, yaml, os

app = Flask(__name__)

if 'flask' in onb.conf:
	app.config.update(**onb.conf.flask)

onb.app = app
onb.api = Api(app, errors=errors, catch_all_404s=True)
onb.jwt = JWTManager(app)

from api.common.converters import url_converters
onb.app.url_map.converters = {**onb.app.url_map.converters, **url_converters}

from api.common.auth import *
from api.ressources import *

@onb.app.before_request
def _db_connect():
	if onb.sqldb.is_closed():
		onb.sqldb.connect()

@onb.app.teardown_request
def _db_close(exc):
	if not onb.sqldb.is_closed():
		onb.sqldb.close()

@onb.api.resource('/')
class ApiReference(Resource):
	def get(self):
		filename = os.path.join(onb.OnbSettings.root, 'api/swagger_doc.yml')

		with open(filename, 'r') as f:
			return yaml.load(f)