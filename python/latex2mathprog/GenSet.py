from GenObjWithSubIndices import *

class GenSet(GenObjWithSubIndices):
	def __init__(self, name, dimen = 1, firstStmt = None, lastStmt = None, certainty = True, isDeclaredAsSet = False):
		super(GenSet, self).__init__(name, firstStmt, lastStmt)
		self.dimen = dimen
		self.certainty = certainty
		self.isDeclaredAsSet = isDeclaredAsSet
	
	def getDimension(self):
		return self.dimen

	def setDimension(self, dimen):
		self.dimen = dimen

	def getCertainty(self):
		return self.certainty

	def setCertainty(self, certainty):
		self.certainty = certainty

	def getIsDeclaredAsSet(self):
		return self.isDeclaredAsSet

	def setIsDeclaredAsSet(self, isDeclaredAsSet):
		self.isDeclaredAsSet = isDeclaredAsSet
