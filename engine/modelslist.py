from .models import *
from .datas.datamodel import DataModel

modelsList = {}

def _addSubClasses(classname):
	for modelClass in classname.__subclasses__():
		name = modelClass.getModelName()
		modelsList[name] = modelClass
		_addSubClasses(modelClass)
_addSubClasses(DataModel)


def getModelByName(name):
	return modelsList[name]

def initModelByName(name, *params):
	return modelsList[name](*params)