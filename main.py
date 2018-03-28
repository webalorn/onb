#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from engine.models.creature import DataCreature

try:
	creature = DataCreature()
	print(creature)
	print(creature['armor.protection'])
	creature['armor.protection'] = 12

	for field in creature:
		print(field, creature[field])
except AttributeError as error1:
	print('Mauvaise valeur', error1.args)
except ValueError as error2:
	print('Erreur de valeur', error2.args)
except KeyError as error2:
	print('Erreur d\'indice', error2.args)