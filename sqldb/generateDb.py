import env.dev.settings, onb, peewee
from sqldb.models import *

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

from engine.models.creature import *
generateBaseDatas()

sqlCreature = gameobject.sqlModels['creature']

creature = CreatureModel()
creature.name = "Coooonaaaan !"
creature.health = 42
sqlCreature.create(owner_id=1, model=creature)

ability = AbilityModel()
ability.parry = 666
gameobject.sqlModels['ability'].create(owner_id=1, model=ability)

"""c = sqlCreature.get(id=1)
c.model.name = "Kro"
print(c.model)
c.save()"""