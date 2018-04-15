import env.dev.settings
from sqldb.db import *

generateStructure(verbose=True)

from engine.models.gameentities import *

def generateLines():
	sqlCreature = gameobject.sqlModels['unit']

	vals = ["space gobelin", "space goblin", "gobelin", "gobelin terrestre", "créature terrestre"]

	for description in vals:
		creature = UnitModel()
		creature.name = "Coooonaaaan !"
		creature.health = 42
		creature.summary = description
		c = sqlCreature.create(model=creature)

generateLines()