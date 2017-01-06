class GenSubIndice:

	def __init__(self, indice, name, stmtIndex, order, orderInStmt, domain = None, varType = None, parent = None, minVal = float('inf'), maxVal = -float('inf')):
		self.indice = indice
		self.name = name
		self.stmtIndex = stmtIndex
		self.domain = domain
		self.varType = varType
		self.parent = parent
		self.minVal = minVal
		self.maxVal = maxVal
		self.order = order
		self.orderInStmt = orderInStmt

	def getIndice(self):
		return self.indice

	def setIndice(self, indice):
		self.indice = indice

	def getOrder(self):
		return self.order

	def setOrder(self, order):
		self.order = order

	def getOrderInStmt(self):
		return self.orderInStmt

	def setOrderInStmt(self, orderInStmt):
		self.orderInStmt = orderInStmt

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

	def getStmtIndex(self):
		return self.stmtIndex

	def setStmtIndex(self, stmtIndex):
		self.stmtIndex = stmtIndex
