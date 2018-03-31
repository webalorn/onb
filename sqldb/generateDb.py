#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from models import *
import onb

tables = []

def _addSubModels(classname):
	for modelClass in classname.__subclasses__():
		tables.append(modelClass)
		_addSubModels(modelClass)
_addSubModels(basemodels.TableModel)

print("Create tables for:", tables)
onb.sqldb.create_tables(tables)

from engine.models.creature import *
def tests():
	creature = CreatureModel()
	creature.name = "GroGro"

	try:
		uc = gameobjects.GameObject
		uc.create(username="root")
	except:
		pass

	m = gameobjects.GameObject.createFrom(creature, user_id=1)
	print(m.getModel())
	m.save()

tests()