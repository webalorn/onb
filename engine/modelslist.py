from .models import *
from .datas.datamodel import DataModel

modelsList = {}

for modelClass in DataModel.__subclasses__():
	name = modelClass.getModelName()
	modelsList[name] = modelClass


def getModelByName(name):
	return modelsList[name]

def initModelByName(name, *params):
	return modelsList[name](*params)