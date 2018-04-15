from flask_restful import Resource
from engine.storage.jsondb import readDatasFrom
import onb

@onb.api.resource('/model/table')
class GameTableModel(Resource):
	def get(self):
		return {
			'model': readDatasFrom(onb.conf.game.locations.table)
		}