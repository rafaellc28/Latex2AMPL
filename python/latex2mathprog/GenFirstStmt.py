from GenObj import *

class GenFirstStmt(GenObj):
	def __init__(self, name, firstStmt):
		super(GenFirstStmt, self).__init__(name)
		self.firstStmt = firstStmt

	def getFirstStmt(self):
		return self.firstStmt

	def setFirstStmt(self, firstStmt):
		if int(firstStmt) < self.firstStmt:
			self.firstStmt = firstStmt
