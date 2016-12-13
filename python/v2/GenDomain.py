from GenObj import *

class GenDomain(GenObj):
	def __init__(self, name, stmtIndex, order, domain = None):
		super(GenDomain, self).__init__(name)
		self.stmtIndex = stmtIndex
		self.order = order
		self.domain = domain

	def getStmtIndex(self):
		return self.stmtIndex

	def setStmtIndex(self, stmtIndex):
		self.stmtIndex = stmtIndex

	def getOrder(self):
		return self.order
	
	def setOrder(self, indice):
		self.order = order

	def getDomain(self):
		return self.domain

	def setDomain(self, domain):
		self.domain = domain
