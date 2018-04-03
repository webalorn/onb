import os, random, string
from peewee import SqliteDatabase

root = os.path.dirname(__file__)

### Global configuration
class conf:
	DICES = [0, 4, 6, 8, 10, 12, 20, 100]
	debug = True
	dbFilesLocation = os.path.join(root, 'db/files')
	sqliteDbLocation = os.path.join(root, 'db/onb.db')
	cacheAllModels = False # Avoid duplicate instances of the same model, but keep the model in memory

### Environment creation

os.makedirs(os.path.dirname(conf.sqliteDbLocation), exist_ok=True)

### Global variables

sqldb = SqliteDatabase(conf.sqliteDbLocation)
api = None

### Global utility functions

class Utility:
	def randomString(size=10):
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

### Global functions for simple parameters use

def getDbPath(filename, *params, newFile=False):
	directory = os.path.join(conf.dbFilesLocation)
	os.makedirs(directory, exist_ok=True)
	path = os.path.join(conf.dbFilesLocation, filename)

	if newFile:
		generatedPath = path
		while os.path.isfile(generatedPath):
			generatedPath = path.split('.')
			generatedPath[0] += '_' + Utility.randomString()
			generatedPath = '.'.join(generatedPath)
		path = generatedPath

	return path