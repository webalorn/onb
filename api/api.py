from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from api.common.errors import errors
import onb, env.dev.settings, os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'dev_secret_key'
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_ALGORITHM'] = 'HS512'

onb.app = app
onb.api = Api(app, errors=errors)
onb.jwt = JWTManager(app)

from api.common.converters import *
from api.common.auth import *
from api.ressources import *

@onb.app.before_request
def _db_connect():
	onb.sqldb.connect()

@onb.app.teardown_request
def _db_close(exc):
	if not onb.sqldb.is_closed():
		onb.sqldb.close()

@onb.api.resource('/')
class HelloWorld(Resource):
	def get(self):
		return {'hello': 'the world'}

if __name__ == '__main__':
	#app.run(debug=onb.conf.debug)
	app.run(debug=True)