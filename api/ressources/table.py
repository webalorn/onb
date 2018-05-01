from flask_restful import Resource
import onb

@onb.api.resource('/model/table')
class GameTableModel(Resource):
	def get(self):
		return {
			'model': onb.conf.game.table_json
		}