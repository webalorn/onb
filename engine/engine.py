import random, string

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class Rand:
	def randomString(size=10):
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

	def roll(diceValue):
		return random.randint(1, diceValue)