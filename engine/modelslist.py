from .models import *

modelsList = {
	'creature' : creature.CreatureModel,
	'armor' : creature.ArmorModel,
}



def getModelByName(name):
	return modelsList[name]

def initModelByName(name, *params):
	return modelsList[name](*params)