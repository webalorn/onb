import onb, env.dev.settings

from engine.models.creature import *
from engine.models.gameentities import GameEntityModel
from engine.models.tables import *

from engine.modelslist import modelsList
from engine.datas.populate import PopulateManager
from engine.storage.encoder import ModelEncoder
from engine.modelslist import modelsList
from engine.storage.sheet import *
from engine.storage.manager import StorageManager
import engine.storage.jsondb as jdb

import pprint
import copy

try:
	print("Dices:", *onb.conf.DICES)
	#print(modelsList['dammage_table'])
	creature = CreatureModel()
	PopulateManager().populate(creature, {"name":"Conan", "actions.10":{'type':'action_move'}, 'protection.ice_bonus': 12})
	print(creature.get('protection.ice_bonus', 0))
	print(ModelEncoder.encode(creature))

	print(creature.actions.getMaxKey())
	creature.actions.append(AttackModel({'weapon_name':'Very big sword'}))
	print(creature.actions.getList())

	#d = DammageTableModel()
	#PopulateManager().populate(d, {"values": [0, 1, 42]})
	#print(d.values)

	#sm = StorageManager()
	#creature = sm.load('creature.json')
	#sm.save(creature)
	#print(creature.protection)
except KeyError as error2:
	raise error2
	print('Erreur d\'indice', error2.args)