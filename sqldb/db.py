import peewee, onb
from sqldb.models import *
import engine.storage.jsondb as jsondb
from engine.generator.tables import TableGenerator

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
	try:
		user.User.create(username="root")
	except peewee.IntegrityError:
		print("Base datas have already been generated")

	jsondb.storeTo(TableGenerator.new(), onb.conf.game.locations.table)
	onb.sqldb.close()