import random

class Rand:
	def randomString(size=10):
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

	def roll(diceValue):
		return random.randint(1, diceValue)