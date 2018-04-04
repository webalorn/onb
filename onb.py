import os, string
from peewee import SqliteDatabase
from engine.rand import Rand

root = os.path.dirname(__file__)

### Global configuration
conf, sqldb, api = None, None, None

class OnbSettings:
	DICES = [0, 4, 6, 8, 10, 12, 20, 100]
	debug = False
	cacheAllModels = False # Avoid duplicate instances of the same model, but keep the model in memory

	dbRootLocation = os.path.join(root, 'db')
	dbFilesLocation = os.path.join(dbRootLocation, 'files')
	sqliteDbLocation = os.path.join(dbRootLocation, 'onb.db')


	def createDbObject(self):
		os.makedirs(os.path.dirname(self.sqliteDbLocation), exist_ok=True)
		return SqliteDatabase(self.sqliteDbLocation)

	def __init__(self):
		global conf, sqldb, api
		sqldb = self.createDbObject()
		conf = self

### Global functions for simple parameters use

def getDbPath(filename, *params, newFile=False):
	directory = os.path.join(conf.dbFilesLocation)
	os.makedirs(directory, exist_ok=True)
	path = os.path.join(conf.dbFilesLocation, filename)

	if newFile:
		generatedPath = path
		while os.path.isfile(generatedPath):
			generatedPath = path.split('.')
			generatedPath[0] += '_' + Rand.randomString()
			generatedPath = '.'.join(generatedPath)
		path = generatedPath

	return path