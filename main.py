#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))

from engine.models.creature import *
from engine.modelslist import modelsList
from engine.datas.populate import PopuplateManager
from engine.storage.encoder import *
from engine.modelslist import modelsList
from engine.storage.sheet import *

import pprint
import copy

import engine.settings as conf

try:
	print("Dices:", *conf.DICES)
	creature = CreatureModel()
	PopuplateManager().populate(creature, {"actions.attacks.main_weapon":{}, 'protection.ice_bonus': 12})

	datas1 = ModelEncoder().encode(creature)
	datas2 = ModelEncoder().linearize(datas1)
	#pprint.pprint(datas2)

	tables = DiceTableModel()
	tables['values']['-10'] = 3
	tables['values']['4'] = 3
	tables['values'].setKeysRange(range(8))

	tables2 = copy.deepcopy(tables)

	tables['values']['0'] = 100

	pprint.pprint(ModelEncoder().encode(tables))
	pprint.pprint(ModelEncoder().encode(tables2))

	conv = SheetConverter()
	"""conv.addColumn(creature)
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