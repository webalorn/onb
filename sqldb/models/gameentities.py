from .gameobject import *

### Tables

"""class DammageTable(GameObject, TableModel):
	modelClass = 'dammage_table'
	
	def populateFields(self, model):
		
		super().populateFields(model)"""

### Entities

class GameEntity(GameObject, TableModel):
	modelClass = 'creature'

	name = TextField()
	alignment = TextField()
	race = TextField()

	def populateFields(self, model):
		self.name = model.name
		self.alignment = model.alignment
		self.race = model.race
		super().populateFields(model)