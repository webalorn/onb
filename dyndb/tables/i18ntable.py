from ..basedyntable import BaseDynTable
from engine.engine import Rand
import re

argReg = re.compile('^[a-zA-Z0-9_]+$')

class I18nDynTable(BaseDynTable):
	"""
		Key format: key_user_id:lang
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
		if len(keys) > 100:
			return {**getMultiple(keys[:100], lang, default), **getMultiple(keys[100:], lang, default)}
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

	def set(self, key, lang, translation):
		for arg in (key, lang):
			if not argReg.match(str(arg)):
				raise ValueError
		dbKey = key + ':' + str(lang)
		self.table.put_item(
			Item={
				'key': dbKey,
				'translation': str(translation),
			}
		)
		return key

	def setMultiple(self, key, translations):
		for lang, text in translations.items():
			self.set(key, lang, text)

	def newKey(self, user_id):
		return Rand.randomString(20) + '_' + str(user_id)

	def new(self, user_id, lang, translation):
		return self.set(self.newKey(user_id), lang, translation)

	def delete(self, key, lang):
		table.delete_item(
			Key={
				'key': str(key) + ':' + str(lang),
			}
		)