from flask_restful import Resource, reqparse, marshal, marshal_with, request
from sqldb.models.battle import Battle as sqlBattle
from sqldb.models.battle import Army as sqlArmy
from api.common.parser import ExtendedParser
import flask_jwt_extended as fjwt
from api.common.errors import *
from api.common.common import *
from api.fields.battles import *
import onb, peewee

def getBattleArgs():
	parser = ExtendedParser()
	parser.add_argument('universe', type=str, choices=[None] + onb.conf.game.universes)
	parser.add_argument('battleground', type=str)
	parser.add_argument('allow_cross_alignment', type=bool)
	parser.add_argument('name', type=str)
	parser.add_argument('scenario', type=str)
	parser.add_argument('army_maximum_cost', type=int)

	args = parser.parse_args()

	if 'army_maximum_cost' in args:
		if args['army_maximum_cost'] < 0:
			raise BadRequestError

	return args;

def getArmyArgs():
	parser = ExtendedParser()
	parser.add_argument('name', type=str)
	parser.add_argument('aglignement', type=str)

	args = parser.parse_args()
	return args;

"""
Common functions
"""

def getPlayerBattle(battle_id, mustBePlayer=True):
	battle = sqlBattle.get(id=battle_id)
	if mustBePlayer and not battle.isPlayerAllowed(fjwt.get_current_user().id):
		raise NotFoundError
	return battle

def getPlayerArmy(army_id, mustBePlayer=True):
	army = sqlArmy.get(id=army_id)
	if mustBePlayer and not army.isPlayerAllowed(fjwt.get_current_user().id):
		raise NotFoundError
	return army

"""
Model Endpoints
"""

@onb.api.resource('/battle')
class Battle(Resource):
	@fjwt.jwt_required
	@marshal_with(battle_fields_short)
	def get(self):
		return list(fjwt.get_current_user().getBattles())

	@fjwt.jwt_required
	@marshal_with(battle_fields_short)
	def post(self):
		battle = sqlBattle.create(
			owner_id=fjwt.get_current_user().id,
			**getBattleArgs(),
		)
		return battle

@onb.api.resource('/battle/<int:id>')
class BattleById(Resource):
	@fjwt.jwt_required
	@marshal_with(battle_fields)
	def get(self, id):
		return getPlayerBattle(id)

	@fjwt.jwt_required
	@marshal_with(battle_fields)
	def put(self, id):
		battle = getPlayerBattle(id)
		battle.updateFrom(getBattleArgs())
		return battle

	@fjwt.jwt_required
	def delete(self, id):
		getPlayerBattle(id).delete_instance()

@onb.api.resource('/battle/<int:battle_id>/user/<int:user_id>')
class BattleUsers(Resource):
	@fjwt.jwt_required
	def put(self, battle_id, user_id):
		battle = getPlayerBattle(battle_id)
		battle.addPlayer(user_id)
		battle.save()

	@fjwt.jwt_required
	def delete(self, battle_id, user_id):
		battle = getPlayerBattle(battle_id)
		battle.removePlayer(user_id)
		battle.save()

@onb.api.resource('/battle/<int:battle_id>/armies')
class BattleArmies(Resource):
	@fjwt.jwt_required
	@marshal_with(army_fields)
	def get(self, battle_id):
		return list(getPlayerBattle(battle_id).armies)

	@fjwt.jwt_required
	@marshal_with(army_fields)
	def post(self, battle_id):
		battle = getPlayerBattle(battle_id)
		return sqlArmy.create(
			battle_id=battle.id,
			**getArmyArgs(),
		)
		battle.save()

@onb.api.resource('/army/<int:id>')
class BattleArmy(Resource):
	@fjwt.jwt_required
	@marshal_with(army_fields)
	def get(self, id):
		return getPlayerArmy(id)

	@fjwt.jwt_required
	@marshal_with(army_fields)
	def put(self, id):
		army = getPlayerArmy(id)
		army.updateFrom(getArmyArgs())
		return army

	@fjwt.jwt_required
	def delete(self, id):
		getPlayerArmy(id).delete_instance()

@onb.api.resource('/army/<int:army_id>/unit/<int:unit_id>')
class ArmyUnit(Resource):
	@fjwt.jwt_required
	def put(self, army_id, unit_id):
		count = int(request.get_json())
		army = getPlayerArmy(army_id)
		army.setUnitCount(unit_id, count)
		army.save()

	@fjwt.jwt_required
	def delete(self, army_id, unit_id):
		army = getPlayerArmy(army_id)
		army.removeUnit(unit_id)
		army.save()

