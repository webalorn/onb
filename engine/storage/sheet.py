import copy, math
import pandas as pd
from .encoder import *

class SheetConverter():

	def __init__(self):
		self.clear()
		self.versionId = 0

	def clear(self):
		self.sheets = {}
		self.nbColumns = {}

	def addColumn(self, modelDatas, sheetName='game'):
		if not sheetName in self.sheets:
			self.sheets[sheetName] = {}
			self.nbColumns[sheetName] = 0
		datas = self.sheets[sheetName]

		if not isinstance(modelDatas, dict):
			modelDatas = ModelEncoder().encode(modelDatas)
		modelDatas = copy.deepcopy(modelDatas)
		modelDatas = ModelEncoder().linearize(modelDatas)

		for key in modelDatas:
			if not key in datas:
				datas[key] = [None]*self.nbColumns[sheetName]
		for key in datas:
			datas[key].append(None)
		for key in modelDatas:
			datas[key][self.nbColumns[sheetName]] = modelDatas[key]
		self.nbColumns[sheetName] += 1

	def convertToGrid(self, sheetName):
		datas = self.sheets[sheetName]
		grid = []
		# Line 1: <versionId> <> [<names]
		grid.append([self.versionId, None])
		grid[0] += datas['name'] if 'name' in datas else [None]*self.nbColumns[sheetName]

		# Lines 2-...: <id> <name> [<values]
		for key in datas:
			grid.append([key, key.split('.')[-1]] + datas[key])
		return grid

	def saveTo(self, filePath):
		writer = pd.ExcelWriter(filePath, engine='xlsxwriter')
		for sheetName in self.sheets:
			grid = self.convertToGrid(sheetName)
			
			df = pd.DataFrame(grid)
			df.to_excel(writer, sheet_name=sheetName, index=False, index_label=False, header=False)
		writer.save()

	def readFrom(self, filePath):
		self.clear()
		xl = pd.ExcelFile(filePath)
		for sheetName in xl.sheet_names:
			df = xl.parse(sheetName, header=None)
			grid = df.values.tolist()
			grid = [[None if cell != cell else cell for cell in lig] for lig in grid]

			self.sheets[sheetName] = {}
			self.nbColumns[sheetName] = len(grid[0][2:])

			for line in grid[1:]:
				key = line[0]
				colums = line[2:]
				self.sheets[sheetName][key] = colums

	def getModelDatas(self, sheetName=None):
		if sheetName == None:
			models = []
			for sheetName in self.sheets:
				models += self.getModelDatas(sheetName)
			return models
		else:
			models = [{} for _ in range(self.nbColumns[sheetName])]
			datas = self.sheets[sheetName]
			for key in datas:
				for iModel in range(len(models)):
					if datas[key][iModel] != None:
						models[iModel][key] = datas[key][iModel]
			return models

