from GenObjWithSubIndices import *

class GenParameter(GenObjWithSubIndices):
	def __init__(self, name, isSymbolic = False, firstStmt = None, lastStmt = None, stmtInclusion = None, certainty = True):
		super(GenParameter, self).__init__(name, firstStmt, lastStmt)
		self.isSymbolic = isSymbolic
		self.stmtInclusion = stmtInclusion
		self.certainty = certainty
	
	def getIsSymbolic(self):
		return self.isSymbolic
	
	def setIsSymbolic(self, isSymbolic):
		self.isSymbolic = isSymbolic

	def getStmtInclusion(self):
		return self.stmtInclusion

	def setStmtInclusion(self, stmtInclusion):
		self.stmtInclusion = stmtInclusion

	def getCertainty(self):
		return self.certainty

	def setCertainty(self, certainty):
		self.certainty = certainty
