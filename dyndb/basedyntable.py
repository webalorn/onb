import boto3

class BaseDynTable:
	def __init__(self, table):
		self.table = table