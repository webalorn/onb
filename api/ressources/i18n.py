from flask_restful import Resource, request
from api.common.parser import ExtendedParser
import flask_jwt_extended as fjwt
from api.common.errors import *
import onb

def parseTranslations():
	parser = ExtendedParser()
	for lang in onb.conf.langs:
		parser.add_argument(lang, type=str)
	return parser.parse_args()

def isKeyOwnedBy(key, user_id):
	key = key.split('_')
	if len(key) == 2 and key[1] == str(user_id):
		return True
	return False

def parseKeysList():
	l = request.get_json()
	print("REQ", l)
	if not isinstance(l, list):
		return []
	return [el for el in l if isinstance(el, str)]

def getTable():
	return onb.dyndb.get('i18n')

@onb.api.resource('/i18n')
class I18nMain(Resource):
	@fjwt.jwt_required
	def post(self):
		user = fjwt.get_current_user()
		key = getTable().newKey(user.id)
		getTable().setMultiple(key, parseTranslations())
		return key

@onb.api.resource('/i18n/key/<string:key>')
class I18nUpdateKey(Resource):
	@fjwt.jwt_required
	def put(self, key):
		if isKeyOwnedBy(key, fjwt.get_current_user().id):
			getTable().setMultiple(key, parseTranslations())
		else:
			raise NotFoundError

@onb.api.resource('/i18n/<lang:lang>')
class I18nLang(Resource):
	def get(self, lang):
		keys = parseKeysList()
		if keys:
			return getTable().getMultiple(keys, lang)
		return {}

@onb.api.resource('/i18n/<lang:lang>/<string:key>')
class I18nLangKey(Resource):
	def get(self, lang, key):
		return getTable().get(key, lang)

	@fjwt.jwt_required
	def put(self, lang, key):
		if isKeyOwnedBy(key, fjwt.get_current_user().id):
			getTable().set(key, lang, str(request.get_json()))
		else:
			raise NotFoundError