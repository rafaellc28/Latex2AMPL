from GenObj import *

class GenDomain(GenObj):
	def __init__(self, name, domain = None):
		super(GenDomain, self).__init__(name)
		self.domain = domain

	def getDomain(self):
		return self.domain

	def setDomain(self, domain):
		self.domain = domain
