#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, peewee
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from sqldb.models import *
import onb

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
c = sqlCreature.get(id=2)
c.model.name = "Kro"
print(c.model)
c.save()

"""creature = CreatureModel()
creature.name = "Coooonaaaan !"
sqlCreature.create(owner_id=1, model=creature)"""