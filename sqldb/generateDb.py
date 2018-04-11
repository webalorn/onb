import env.dev.settings, onb, peewee
from sqldb.models import *

import engine.storage.jsondb as jsondb
from engine.generator.tables import TableGenerator

tables = []

### Create a table for all subclasses of TableModel

def _addSubModels(classname):
	for modelClass in classname.__subclasses__():
		tables.append(modelClass)
		_addSubModels(modelClass)
_addSubModels(basemodels.TableModel)

print("Create tables for:", [t.__name__ for t in tables])
onb.sqldb.create_tables(tables)

def generateBaseDatas():
	try:
		basemodels.User.create(username="root")
	except peewee.IntegrityError:
		print("Base datas have already been generated")

	jsondb.storeTo(TableGenerator.new(), onb.conf.game.locations.table)

generateBaseDatas()

from engine.models.gameentities import *

def generateLines():
	sqlCreature = gameobject.sqlModels['unit']

	creature = UnitModel()
	creature.name = "Coooonaaaan !"
	creature.health = 42
	c = sqlCreature.create(model=creature)

generateLines()