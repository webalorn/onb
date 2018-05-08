import onb, env.dev.settings
import boto3

onb_i18n = onb.dyndb.dynamodb.create_table(
	TableName='onb_i18n',
	KeySchema=[
		{
			'AttributeName': 'key',
			'KeyType': 'HASH'
		},
	],
	AttributeDefinitions=[
		{
			'AttributeName': 'key',
			'AttributeType': 'S'
		},
	],
	ProvisionedThroughput={
		'ReadCapacityUnits': 5,
		'WriteCapacityUnits': 5
	}
)
