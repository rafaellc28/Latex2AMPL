from GenObj import *

class GenDomain(GenObj):
	def __init__(self, name, stmtIndex, order, domain = None, domainObj = None, domainSupObj = None):
		super(GenDomain, self).__init__(name)
		self.stmtIndex = stmtIndex
		self.order = order
		self.domain = domain
		self.domainObj = domainObj
		self.domainSupObj = domainSupObj

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

	def getDomainObj(self):
		return self.domainObj

	def setDomainObj(self, domainObj):
		self.domainObj = domainObj

	def getDomainSupObj(self):
		return self.domainObj

	def setDomainSupObj(self, domainObj):
		self.domainSupObj = domainSupObj
