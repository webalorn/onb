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
	#print(modelsList['dammage_table'])
	creature = CreatureModel()
	PopuplateManager().populate(creature, {"actions.attacks.main_weapon":{}, 'protection.ice_bonus': 12})
	print(creature.get('protection.ice_bonus', 0))

	#sm = StorageManager()
	#creature = sm.load('creature.json')
	#sm.save(creature)
	print(creature)
except KeyError as error2:
	raise error2
	print('Erreur d\'indice', error2.args)