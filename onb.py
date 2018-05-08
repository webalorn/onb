import os
from playhouse.postgres_ext import PostgresqlExtDatabase
from engine.engine import Rand, Map, SettingsLoader
from dyndb.dyndb import DynDb
import psycopg2
from urllib.parse import *

### Global configuration
conf = None
conf, sqldb, dyndb = None, None, None

class OnbSettings:
	"""
		Settings files special fields:
		- require: a dictionary of key: files that will be included as sub-fields
		- inherit
		- locations : a dictionary of locations. Locations will be tranformed to absolute paths
	"""

	root = os.path.dirname(__file__)

	@classmethod
	def createDbObject(self):
		if conf.sqldb == 'heroku':
			DATABASE_URL = os.environ.get('DATABASE_URL')
			db = urlparse(DATABASE_URL)
			user = db.username
			password = db.password
			path = db.path[1:]
			host = db.hostname
			port = db.port
			return PostgresqlExtDatabase(path, user=user, password=password, host=host, port=port)
		return PostgresqlExtDatabase(conf.sqldb, user='onb', password='onb')

	@classmethod
	def createDynDbObject(cls):
		if conf.dyndb:
			return DynDb(conf.dyntables)
		return None

	@classmethod
	def inMemoryGeneratedDatas(cls):
		from engine.generator.tables import TableGenerator
		from engine.storage.encoder import ModelEncoder

		conf.game.table = TableGenerator.new()
		conf.game.table_json = ModelEncoder.encode(conf.game.table)

	@classmethod
	def loadFrom(cls, filename):
		global conf, sqldb, dyndb
		if conf != None:
			raise RuntimeError("Configuration already loaded")
		cfgLoader = SettingsLoader(cls.root)
		conf = cfgLoader.loadYamlCfg(filename)

		sqldb = cls.createDbObject()
		dyndb = cls.createDynDbObject()
		cls.inMemoryGeneratedDatas()

### Global functions for simple parameters use

def getDbPath(filename, *params, newFile=False):
	directory = conf.locations.dbFiles
	os.makedirs(directory, exist_ok=True)
	path = os.path.join(conf.locations.dbFiles, filename)

	if newFile:
		generatedPath = path
		while os.path.isfile(generatedPath):
			generatedPath = path.split('.')
			generatedPath[0] += '_' + Rand.randomString()
			generatedPath = '.'.join(generatedPath)
		path = generatedPath

	return path
