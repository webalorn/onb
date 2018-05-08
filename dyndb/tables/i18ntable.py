from ..basedyntable import BaseDynTable
from engine.engine import Rand
import re

argReg = re.compile('^[a-zA-Z0-9_]+$')

class I18nDynTable(BaseDynTable):
	"""
		Key format: id:user_id:lang
	"""
	def translate(self, key, lang):
		key = str(key) + ':' + str(lang)
		response = self.table.get_item(
			Key={
				'key': key,
			}
		)
		if not 'Item' in response or not 'translation' in response['Item']:
			if lang != 'en':
				return translate(self, key, 'en')
			raise KeyError
		return response['Item']['translation']

	def get(self, key, lang, default=''):
		""" Get a translation OR default value """
		try:
			return self.translate(key, lang)
		except KeyError:
			return default

	def getMultiple(self, keys, lang, default=''):
		import onb
		dbKeys = [str(key) + ':' + str(lang) for key in keys]
		if lang != 'en':
			dbKeys += [str(key) + ':en' for key in keys]

		response = onb.dyndb.dynamodb.batch_get_item(
			RequestItems={
				self.table.name: {
					'Keys': [{'key': val} for val in dbKeys],
					'AttributesToGet': [
						'key',
						'translation',
					],
				}
			},
		)
		responseValues = response['Responses'][self.table.name]
		translations = {r['key'] : r['translation'] for r in responseValues}

		finalTranslations = {}
		for key in keys:
			langKey = str(key) + ':' + lang
			enKey = str(key) + ':en'
			if langKey in translations:
				finalTranslations[key] = translations[langKey]
			elif enKey in translations:
				finalTranslations[key] = translations[enKey]
			else:
				finalTranslations[key] = default

		return finalTranslations

	def set(self, key, user_id, lang, translation):
		for arg in (key, user_id, lang):
			if not argReg.match(str(arg)):
				raise ValueError
		key = str(key) + ':' + str(user_id)
		dbKey = key + ':' + str(lang)
		self.table.put_item(
			Item={
				'key': dbKey,
				'translation': str(translation),
			}
		)
		return key

	def new(self, user_id, lang, translation):
		return self.set(Rand.randomString(20), user_id, lang, translation)

	def delete(self, key, user_id, lang):
		table.delete_item(
			Key={
				'key': str(key) + ':' + str(user_id) + ':' + str(lang),
			}
		)