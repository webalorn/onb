#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from engine.models.creature import CreatureModel
from engine.modelslist import modelsList
from engine.datas.populate import PopuplateManager
from engine.storage.encoder import *
from engine.modelslist import modelsList

import pprint

print(modelsList)

try:
	creature = CreatureModel()
	PopuplateManager().populate(creature, {"actions.attacks.main_weapon":{}, 'protection.ice_bonus': 12})

	datas1 = ModelEncoder().encode(creature)
	datas2 = ModelEncoder().linearize(datas1)
	pprint.pprint(datas2)

	#creature2 = ModelEncoder().decode(datas2)
	#print(creature2)
except KeyError as error2:
	raise error2
	print('Erreur d\'indice', error2.args)