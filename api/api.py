from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from api.common.errors import errors
import onb, env.dev.settings, os

app = Flask(__name__)

if 'flask' in onb.conf:
	for key in onb.conf.flask:
		app.config[key] = onb.conf.flask[key]

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