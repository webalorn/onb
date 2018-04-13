from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from api.common.errors import errors
import onb, env.dev.settings, os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'dev_secret_key'

onb.app = app
onb.api = Api(app, errors=errors)
onb.jwt = JWTManager(app)

from api.common.utils import *
from api.common.auth import *
from api.ressources import *

@onb.api.route('/')
class HelloWorld(Resource):
	def get(self):
		return {'hello': 'the world'}

if __name__ == '__main__':
	app.run(debug=onb.conf.debug)