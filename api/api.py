from flask import Flask
from flask_restful import Resource, Api
import onb, env.dev.settings
from api.common.utils import utilsMain
from api.common.errors import errors

app = Flask(__name__)
api = Api(app, errors=errors)

onb.app = app
onb.api = api

utilsMain()

from api.ressources import *

@api.route('/')
class HelloWorld(Resource):
	def get(self):
		return {'hello': 'the world'}

if __name__ == '__main__':
	app.run(debug=onb.conf.debug)