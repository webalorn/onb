import peewee, onb
from sqldb.models import *
from sqldb.models.user import User
import engine.storage.jsondb as jsondb

tables = []

def _addSubModels(classname):
	for modelClass in classname.__subclasses__():
		tables.append(modelClass)
		_addSubModels(modelClass)
_addSubModels(basemodels.SqlTableModel)

def generateStructure(verbose=False):
	onb.sqldb.connect()

	if verbose:
		print("Create tables for:", [t.__name__ for t in tables])
	onb.sqldb.create_tables(tables)

	onb.sqldb.close()

def generateBaseTestDatas():
	""" Generate base data for manual or unit testing """
	if onb.sqldb.is_closed():
		onb.sqldb.connect()

	unitModel = gameobject.sqlModels['unit']
	user = User.create(username="test_user", password_hash=User.hashPassword('1234'))

	descriptions = ["space gobelin", "space goblin", "gobelin", "fantastic goblin", "fantastic creature", "gob gob gobelin"]
	for k in range(len(descriptions)):
		unitModel.create(model={'name':'unit'+str(k+1), 'health':k, 'description':descriptions[k]}, owner_id=user.id,
			is_official=(k >= 2), is_public=(k != 5))

	if not onb.sqldb.is_closed():
		onb.sqldb.close()

	return user