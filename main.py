#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from engine.models.creature import CreatureModel
from engine.modelslist import modelsList

try:
	creature = CreatureModel()
	print(creature)
	print(creature['armor.protection'])
	creature['armor.protection'] = 12
	creature['actions.test'] = 32
	print(creature['actions.test'])

	for field in creature:
		print(field, creature[field])
except KeyError as error2:
	print('Erreur d\'indice', error2.args)