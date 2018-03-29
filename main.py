#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from engine.models.creature import CreatureModel
from engine.modelslist import modelsList
from engine.datas.populate import PopuplateManager

try:
	creature = CreatureModel()
	PopuplateManager().populate(creature, {'health': 31, 'name': 'foo', 'floatValue': '4.10', 'armor.protection': '10','actions.db': 10})

	print(creature)
	# creature['armor.protection'] = 12
	# creature['actions.test'] = 32
	# print(creature['actions.test'])

	for field in creature:
		print(field, creature[field])
except KeyError as error2:
	raise error2
	print('Erreur d\'indice', error2.args)