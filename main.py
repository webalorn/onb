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
	creature = CreatureModel({"name":"Conan", "actions.10":{'_type':'action_move'}, 'protection.ice_bonus': 12})
	print(creature.get('protection.ice_bonus', 0))
		
	creature.actions.append(ActionMoveModel({'run_speed':12}))
	creature.actions.append(AttackModel({'weapon_name': 'BIG SWORD'}))
	creature.actions.append(AttackModel({'weapon_name': 'VERY BIG SWORD'}))

	pprint.pprint(creature.actions.filter('attack'))

	encoding = ModelEncoder.encode(creature)
	creature2 = ModelEncoder.decode(encoding)
	print(creature2)

	#print(creature)
	#pprint.pprint(ModelEncoder.encode(creature))
	#pprint.pprint(ModelEncoder.encodeTypes(creature))

except KeyError as error2:
	raise error2
	print('Erreur d\'indice', error2.args)