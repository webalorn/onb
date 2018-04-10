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
	defaultValues = {
		"alignement": ["neutral", "good", "evil"],
		"race": ["human", "elf", "orc", "dwarf"],
	}

	try:
		basemodels.User.create(username="root")

		for field in defaultValues:
			for val in defaultValues[field]:
				basemodels.Value.create(field_name=field, value=val, owner_id=1, is_public=True)
	except peewee.IntegrityError:
		print("Base datas have already been generated")

	jsondb.storeTo(TableGenerator.new(), onb.conf.game.locations.table)

generateBaseDatas()