from GenObj import *

class GenDeclaration(GenObj):
	def __init__(self, name, attributeList = None, indexingExpression = None, subIndices = [], stmtIndex = None):
		super(GenDeclaration, self).__init__(name)
		self.attributeList = attributeList
		self.indexingExpression = indexingExpression
		self.stmtIndex = stmtIndex

		# python bug
		if not subIndices or len(subIndices) == 0:
			self.subIndices = []
		else:
			self.subIndices = subIndices
	
	def getStmtIndex(self):
		return self.stmtIndex
	
	def setStmtIndex(self, stmtIndex):
		self.stmtIndex = stmtIndex

	def getSubIndices(self):
		return self.subIndices
	
	def setSubIndices(self, subIndices):
		self.subIndices = subIndices
	
	def getAttributeList(self):
		return self.attributeList
		
	def setAttributeList(self, attributeList):
		self.attributeList = attributeList

	def addAttributes(self, attributes):
		if self.attributeList == None:
			self.attributeList = []

		if isinstance(attributes, list):
			self.attributeList += attributes
		else:
			self.attributeList.append(attributes)

	def getIndexingExpression(self):
		return self.indexingExpression
			
	def setIndexingExpression(self, indexingExpression):
		self.indexingExpression = indexingExpression

	def getByOp(self, op):
		return filter(lambda el: el.op == op, self.attributeList)

	def getValueByOp(self, op):
		values = self.getByOp(op)

		if values != None and len(values) > 0:
			return values[-1]

		return None

	def getValue(self):
		return self.getValueByOp(":=")

	def getDefault(self):
		return self.getValueByOp("default")

	def getDimen(self):
		return self.getValueByOp("dimen")
	
	def getWithin(self):
		return self.getByOp("within")

	def getIn(self):
		values = self.getByOp("in")
		#inDeclr = filter(lambda el: not el.attribute.startsWith("integer") and not el.attribute.startsWith("binary") and not el.attribute.startsWith("symbolic"), values)
		
		if values != None and len(values) > 0:
			return values

		return []

	def getRelationsEqualTo(self):
		return self.getByOp("=")

	def getRelationsLessThan(self):
		return self.getByOp("<")

	def getRelationsLessThanOrEqualTo(self):
		return self.getByOp("<=")

	def getRelationsGreaterThan(self):
		return self.getByOp(">")

	def getRelationsGreaterThanOrEqualTo(self):
		return self.getByOp(">=")

	def getRelationsDifferentFrom(self):
		return self.getByOp("!=")

	def getRelations(self):
		values  = self.getRelationsEqualTo()
		values += self.getRelationsLessThan()
		values += self.getRelationsLessThanOrEqualTo()
		values += self.getRelationsGreaterThan()
		values += self.getRelationsGreaterThanOrEqualTo()
		values += self.getRelationsDifferentFrom()

		if values != None and len(values) > 0:
			return values

		return None

	def getRelationEqualTo(self):
		values = self.getRelationsEqualTo()

		if values != None and len(values) > 0:
			return values[-1]

		return None

	def getRelationLessThan(self):
		values = self.getRelationsLessThan()

		if values != None and len(values) > 0:
			return values[-1]

		return None

	def getRelationLessThanOrEqualTo(self):
		values = self.getRelationsLessThanOrEqualTo()

		if values != None and len(values) > 0:
			return values[-1]

		return None

	def getRelationGreaterThan(self):
		values = self.getRelationsGreaterThan()

		if values != None and len(values) > 0:
			return values[-1]

		return None

	def getRelationGreaterThanOrEqualTo(self):
		values = self.getRelationsGreaterThanOrEqualTo()

		if values != None and len(values) > 0:
			return values[-1]

		return None

	def getRelationDifferentFrom(self):
		values = self.getRelationsDifferentFrom()

		if values != None and len(values) > 0:
			return values[-1]

		return None
