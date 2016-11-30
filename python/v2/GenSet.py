from GenObjWithSubIndices import *

class GenSet(GenObjWithSubIndices):
	def __init__(self, name, dimen = 1, firstStmt = None, lastStmt = None):
		super(GenSet, self).__init__(name, firstStmt, lastStmt)
		self.dimen = dimen

	def getDimension(self):
		return self.dimen

	def setDimension(self, dimen):
		self.dimen = dimen
