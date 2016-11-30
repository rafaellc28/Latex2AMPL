from GenSubIndices import *

class GenObjWithSubIndices(object):
	def __init__(self, name, firstStmt = None, lastStmt = None):
		self.name = name
		self.sub_indices = GenSubIndices()
		self.firstStmt = firstStmt
		self.lastStmt = lastStmt
	
	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def getSubIndices(self):
		return self.sub_indices

	def setSubIndices(self, sub_indices):
		self.sub_indices = sub_indices

	def getFirstStmt(self):
		return self.firstStmt

	def setFirstStmt(self, firstStmt):
		self.firstStmt = firstStmt

	def getLastStmt(self):
		return self.lastStmt

	def setLastStmt(self, lastStmt):
		self.lastStmt = lastStmt
