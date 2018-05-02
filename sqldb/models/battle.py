from .basemodels import *
from .user import *
from .customfields import *
from api.common.errors import *
from .gameobject import sqlModels
from peewee import *

sqlUnit = sqlModels["unit"]

class Battle(OwnedObject, SqlTableModel):
	universe = TextField(default=None, null=True)
	battleground = TextField(default='')
	allow_cross_alignment = BooleanField(default=False)
	name = TextField(default="")
	scenario = TextField(default="")
	army_maximum_cost = IntegerField(default=1)

	players = PyDataField(default=[]) # List of ids

	def getPlayersModels(self):
		return User.select().where(User.id << self.players)

	def addPlayer(self, player_id):
		player = User.get(id=player_id) # Ensure model exists
		if not player_id in self.players:
			self.players.append(player_id)

	def removePlayer(self, player_id):
		if player_id in self.players:
			self.players.remove(player_id)

	def isPlayerAllowed(self, playerId):
		return playerId in self.players or playerId == self.owner_id

	def save(self, *p, **pn):
		if not self.owner_id in self.players:
			self.players.append(self.owner_id)
		super().save(*p, **pn)

class Army(BaseModel, SqlTableModel):
	name = TextField(default="")
	alignment = TextField(null=True, default=None)
	units = PyDataField(default={}) # {'unit_id': <unit_count>, ...}
	battle = ForeignKeyField(Battle, backref='armies', on_delete='CASCADE')

	def setUnitCount(self, unit_id, unit_count):
		#unit = sqlUnit.get(id=unit_id) # Ensure model exists
		unit_id = str(unit_id)
		if unit_count < 0:
			raise BadRequestError
		self.units[unit_id] = unit_count
		if unit_count == 0:
			del self.units[unit_id]

	def removeUnit(self, unit_id):
		unit_id = str(unit_id)
		if unit_id in self.units:
			del self.units[unit_id]

	def getUnitModels(self):
		return sqlUnit.select().where(sqlUnit.id << [int(i) for i in self.units.keys()])

	def getCost(self):
		unitList = self.getUnitModels()
		totalCost = 0
		for unit in unitList:
			totalCost += unit.cost * self.units[str(unit.id)]

	def isPlayerAllowed(self, playerId):
		return self.battle.isPlayerAllowed(playerId)

	def save(self, *p, **pn):
		units_ids = [str(unit.id) for unit in self.getUnitModels()]
		self.units = {key:val for key, val in self.units.items() if key in units_ids}
		super().save(*p, **pn)