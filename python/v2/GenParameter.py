from GenObjWithSubIndices import *

class GenParameter(GenObjWithSubIndices):
	def __init__(self, name, isSymbolic = False, firstStmt = None, lastStmt = None):
		super(GenParameter, self).__init__(name, firstStmt, lastStmt)
		self.isSymbolic = isSymbolic
	
	def getConstraintIndice(self):
		return self.constraintIndice

	def setConstraintIndice(self, constraintIndice):
		self.constraintIndice = constraintIndice

	def getIsSymbolic(self):
		return self.isSymbolic

	def setIsSymbolic(self, isSymbolic):
		self.isSymbolic = isSymbolic
