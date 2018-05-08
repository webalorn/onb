import boto3
from .tables.i18ntable import *

class DynDb:
	def __init__(self, tablesTypes):
		self.dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
		self.tables = {}
		for tableName, args in tablesTypes.items():
			self.tables[tableName] = tablesTypesNames[args['type']](self.dynamodb.Table(args['name']))

	def get(self, tableName):
		return self.tables[tableName]

tablesTypesNames = {
	'i18n': I18nDynTable,
}