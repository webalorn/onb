import env.dev.settings
from sqldb.db import *

generateStructure(verbose=True)

from engine.models.gameentities import *

def generateLines():
	sqlCreature = gameobject.sqlModels['unit']

	creature = UnitModel()
	creature.name = "Coooonaaaan !"
	creature.health = 42
	c = sqlCreature.create(model=creature)

generateLines()