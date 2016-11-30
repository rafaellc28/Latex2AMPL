from GenObj import *

class GenDomain(GenObj):
	def __init__(self, name, stmtIndex, domain = None):
		super(GenDomain, self).__init__(name)
		self.stmtIndex = stmtIndex
		self.domain = domain

	def getDomain(self):
		return self.domain

	def setDomain(self, domain):
		self.domain = domain
	
	def getStmtIndex(self):
		return self.stmtIndex

	def setStmtIndex(self, stmtIndex):
		self.stmtIndex = stmtIndex
