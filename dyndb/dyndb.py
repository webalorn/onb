import boto3
from .tables.i18ntable import *

class DynDb:
	def __init__(self, tablesTypes, dbType):
		if dbType == 'online':
			self.dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
		elif dbType == 'local':
			self.dynamodb = boto3.resource('dynamodb', region_name='eu-west-3', endpoint_url="http://localhost:8000")
		else:
			raise ValueError('dbType value is not valid')
		self.tables = {}
		for tableName, args in tablesTypes.items():
			self.tables[tableName] = tablesTypesNames[args['type']](self.dynamodb.Table(args['name']))

	def get(self, tableName):
		return self.tables[tableName]

tablesTypesNames = {
	'i18n': I18nDynTable,
}