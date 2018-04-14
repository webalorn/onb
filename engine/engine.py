import random, string, os, yaml, re, tempfile

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class Rand:
	def randomString(size=10):
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))

	def roll(diceValue):
		return random.randint(1, diceValue)

class Map(dict):
	def __getattr__(*args):
		val = dict.get(*args)
		return Map(val) if type(val) is dict else val

	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__
	__getitem__ = __getattr__

tempFiles = []

class SettingsLoader():
	def __init__(self, basePath):
		self.root = basePath

	def cfgStringRealValue(self, strValue):
		getEnv = lambda v : os.getenv(v.group(1)) or ''
		return re.sub(r'\$\(([a-zA-Z0-9_]+)\)', getEnv, strValue)

	def loadCfgVariables(self, cfg):
		if isinstance(cfg, dict):
			for key in cfg:
				if isinstance(cfg[key], str):
					cfg[key] = self.cfgStringRealValue(cfg[key])
				else:
					self.loadCfgVariables(cfg[key])
		elif isinstance(cfg, list):
			for i in range(len(cfg)):
				if isinstance(cfg[i], str):
					cfg[i] = self.cfgStringRealValue(cfg[i])
				else:
					self.loadCfgVariables(cfg[i])

	def getRealPath(self, path):
		if path == '__temp_dir__':
			tmpDir = tempfile.TemporaryDirectory()
			tempFiles.append(tmpDir)
			return tmpDir.name
		else:
			if not os.path.isabs(path):
				return os.path.join(self.root, path)
		return path

	def loadYamlCfg(self, filename):
		if not os.path.isabs(filename):
			filename = os.path.join(self.root, filename)

		with open(filename, 'r') as f:
			cfg = yaml.load(f)

		if 'require' in cfg:
			for section in cfg['require']:
				cfg[section] = self.loadYamlCfg(cfg['require'][section])
			del cfg['require']

		if 'locations' in cfg:
			for section in cfg['locations']:
				cfg['locations'][section] = self.getRealPath(cfg['locations'][section])

		self.loadCfgVariables(cfg)

		if 'inherit' in cfg:
			cfg = self.mergeCfg(cfg, self.loadYamlCfg(cfg['inherit']))
			del cfg['inherit']

		return Map(cfg)

	def mergeCfg(self, source, destination):
		for key, value in source.items():
			if isinstance(value, dict) or isinstance(value, Map):
				node = destination.setdefault(key, {})
				self.mergeCfg(value, node)
			else:
				destination[key] = value
		return destination