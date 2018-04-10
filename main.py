import onb, env.dev.settings

from engine.models.gameentities import *
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
	unit = UnitModel()
	unit.armor.bonuses.ice = 12
	print(unit.armor.bonuses.get('ice', -1))

except KeyError as error2:
	raise error2
	print('Erreur d\'indice', error2.args)