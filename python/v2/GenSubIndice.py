class GenSubIndice:

	def __init__(self, indice, name, domain = None, varType = None, parent = None, minVal = float('inf'), maxVal = 1):
		self.indice = indice
		self.name = name
		self.domain = domain
		self.varType = varType
		self.parent = parent
		self.minVal = minVal
		self.maxVal = maxVal

	def getIndice(self):
		return self.indice

	def setIndice(self, indice):
		self.indice = indice

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def getDomain(self):
		return self.domain

	def setDomain(self, domain):
		self.domain = domain

	def getVarType(self):
		return self.varType

	def setVarType(self, varType):
		self.varType = varType

	def getParent(self):
		return self.parent

	def setParent(self, parent):
		self.parent = parent

	def getMinVal(self):
		return self.minVal

	def setMinVal(self, minVal):
		self.minVal = minVal

	def getMaxVal(self):
		return self.maxVal

	def setMaxVal(self, maxVal):
		self.maxVal = maxVal

