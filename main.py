#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from engine.models.creature import *
from engine.modelslist import modelsList
from engine.datas.populate import PopuplateManager
from engine.storage.encoder import *
from engine.modelslist import modelsList
from engine.storage.sheet import *
from engine.storage.manager import StorageManager
import engine.storage.jsondb as jdb

import pprint
import copy

import onb

try:
	print("Dices:", *onb.conf.DICES)
	creature = CreatureModel()
	creature.save()
	# PopuplateManager().populate(creature, {"actions.attacks.main_weapon":{}, 'protection.ice_bonus': 12})

	
	# sm.save(creature)

	#jdb.storeTo(creature, onb.getDbPath('test.json', newFile=True))
	#creature = jdb.readModelFrom(onb.getDbPath('test.json'))
	print(creature)

	"""conv = SheetConverter()
	conv.addColumn(creature)
	conv.addColumn(datas1)
	conv.addColumn(datas2, 'test2')

	conv.saveTo('test.xlsx')"""

	"""conv.readFrom('test.xlsx')
	pprint.pprint(conv.getModelDatas())"""

	#creature2 = ModelEncoder().decode(datas2)
	#print(creature2)
except KeyError as error2:
	raise error2
	print('Erreur d\'indice', error2.args)