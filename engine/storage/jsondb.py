import json, os
from .encoder import *

def storeTo(modelDatas, path):
	if not isinstance(modelDatas, dict):
		modelDatas = ModelEncoder().encode(modelDatas)

	os.makedirs(os.path.dirname(path), exist_ok=True)

	with open(path, 'w') as outfile:
		json.dump(modelDatas, outfile)

def readDatasFrom(path):
	with open(path) as file:
		return json.load(file)

def readModelFrom(path):
	return ModelEncoder().decode(readDatasFrom(path))