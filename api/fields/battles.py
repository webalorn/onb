from flask_restful import fields, marshal
from .common_fields import MarshalFields
from sqldb.models.battle import Battle as sqlBattle
from sqldb.models.battle import Army as sqlArmy
from engine.storage.encoder import ModelEncoder
from .gamemodel import model_summary
from .user import user_fields_short

class ArmiesField(fields.Raw):
	def format(self, armies):
		return [marshal(val, army_fields) for val in armies]

class PlayersField(fields.Raw):
	def format(self, battle):
		return [marshal(val, user_fields_short) for val in battle.getPlayersModels()]

class UnitsFields(fields.Raw):
	def format(self, army):
		unitsModels = army.getUnitModels()
		return [{
			'unit': marshal(unit, model_summary),
			'count': army.units[str(unit.id)]
		} for unit in unitsModels]

battle_fields_short = {
	'id': fields.Integer,
	'owner_id': fields.Integer,
	'name': fields.String,
	'battleground': fields.String,
	'allow_cross_alignment': fields.Boolean,
	'scenario': fields.String,
	'army_maximum_cost': fields.Integer,
	'universe': fields.String,
	'players': PlayersField(attribute=(lambda x : x)),
}

battle_fields = {
	**battle_fields_short,
	'armies': ArmiesField,
}

army_fields = {
	'id': fields.Integer,
	'battle_id': fields.Integer,
	'name': fields.String,
	'alignment': fields.String,
	'cost': fields.Integer(attribute=sqlArmy.getCost),
	'units': UnitsFields(attribute=(lambda x : x))
}