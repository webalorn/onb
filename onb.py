import os
from playhouse.pool import PooledSqliteExtDatabase
from engine.engine import Rand, Map, SettingsLoader

### Global configuration
conf = Map()
conf, sqldb = None, None

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
		if conf.sqldb == 'sqlite':
			os.makedirs(os.path.dirname(conf.locations.sqliteDb), exist_ok=True)
			return PooledSqliteExtDatabase(conf.locations.sqliteDb)
		elif conf.sqldb == 'memory':
			return PooledSqliteExtDatabase(':memory:')

	@classmethod
	def loadFrom(cls, filename):
		global conf, sqldb
		cfgLoader = SettingsLoader(cls.root)
		conf = cfgLoader.loadYamlCfg(filename)
		sqldb = cls.createDbObject()


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
