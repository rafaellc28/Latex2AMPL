from GenObj import *

class GenBelongsTo(GenObj):
	def __init__(self, name, stmtIndex):
		super(GenBelongsTo, self).__init__(name)
		self.stmtIndex = stmtIndex

	def getStmtIndex(self):
		return self.stmtIndex

	def setStmtIndex(self, stmtIndex):
		self.stmtIndex = stmtIndex
