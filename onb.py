import os, random, string
from peewee import SqliteDatabase

root = os.path.dirname(__file__)

### Global configuration
class conf:
	DICES = [0, 4, 6, 8, 10, 12, 20, 100]
	dbLocation = os.path.join(root, 'db/files')
	sqliteDbLocation = os.path.join(root, 'db/onb.db')
	cacheAllModels = True # Avoid duplicate instances of the same model, but keep the model in memory


sqldb = SqliteDatabase(conf.sqliteDbLocation)

def randomString(size=10):
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def getDbPath(filename, *params, newFile=False):
	directory = os.path.join(conf.dbLocation)
	os.makedirs(directory, exist_ok=True)
	path = os.path.join(conf.dbLocation, filename)

	if newFile:
		generatedPath = path
		while os.path.isfile(generatedPath):
			generatedPath = path.split('.')
			generatedPath[0] += '_' + randomString()
			generatedPath = '.'.join(generatedPath)
		path = generatedPath

	return path