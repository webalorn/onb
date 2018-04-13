import os, string, yaml
from peewee import SqliteDatabase
from engine.engine import Rand, Map

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
	def mergeCfg(cls, source, destination):
		for key, value in source.items():
			if isinstance(value, dict) or isinstance(value, Map):
				node = destination.setdefault(key, {})
				cls.mergeCfg(value, node)
			else:
				destination[key] = value
		return destination

	@classmethod
	def createDbObject(self):
		os.makedirs(os.path.dirname(conf.locations.sqliteDb), exist_ok=True)
		return SqliteDatabase(conf.locations.sqliteDb)

	@classmethod
	def loadYamlCfg(cls, filename):
		if not os.path.isabs(filename):
			filename = os.path.join(cls.root, filename)

		with open(filename, 'r') as f:
			cfg = yaml.load(f)

		if 'require' in cfg:
			for section in cfg['require']:
				cfg[section] = cls.loadYamlCfg(cfg['require'][section])

		if 'locations' in cfg:
			for section in cfg['locations']:
				if not os.path.isabs(cfg['locations'][section]):
					cfg['locations'][section] = os.path.join(cls.root, cfg['locations'][section])

		if 'inherit' in cfg:
			cfg = cls.mergeCfg(cfg, cls.loadYamlCfg(cfg['inherit']))

		return Map(cfg)

	@classmethod
	def loadFrom(cls, filename):
		global conf, sqldb
		conf = cls.loadYamlCfg(filename)
		sqldb = cls.createDbObject()
		





### Global functions for simple parameters use

def getDbPath(filename, *params, newFile=False):
	directory = os.path.join(conf.locations.dbFiles)
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
