from GenList import *

class GenSubIndices(GenList):
	def __init__(self, parent = None):
		super(GenSubIndices, self).__init__()
		self.parent = parent
	
	def getParent(self):
		return self.parent

	def setParent(self, parent):
		self.parent = parent

	def getByIndice(self, indice):
		_subIndices = filter(lambda el: el.getIndice() == indice, self.getAll())

		#if len(_subIndices) > 0:
		#	return _subIndices[0]

		return _subIndices

	def getByIndiceAndStmt(self, indice, stmtIndex):
		_subIndices = filter(lambda el: el.getIndice() == indice and el.getStmtIndex() == stmtIndex, self.getAll())

		#if len(_subIndices) > 0:
		#	return _subIndices[0]

		return _subIndices

	def getAllSortedByIndice(self, _filter = None):
		result = self.getAllSortedByKey(lambda el: el.getIndice())

		if _filter != None:
			result = filter(_filter, result)

		return result

	def getAllSortedByIndiceDesc(self, _filter = None):
		result = self.getAllSortedByKey(lambda el: -el.getIndice())

		if _filter != None:
			result = filter(_filter, result)

		return result

	def getAllSortedByOrder(self, _filter = None):
		result = self.getAllSortedByKey(lambda el: el.getOrder())

		if _filter != None:
			result = filter(_filter, result)

		return result

	def getAllSortedByOrderDesc(self, _filter = None):
		result = self.getAllSortedByKey(lambda el: -el.getOrder())

		if _filter != None:
			result = filter(_filter, result)

		return result

	def get(self, obj):
		objVal = self.getObjVal(obj)
		if objVal == None:
			return None

		_objs = filter(lambda el: el.getName() == objVal and el.getIndice() == obj.getIndice() and el.getStmtIndex() == obj.getStmtIndex() and el.getOrder() == obj.getOrder(), self.vector)

		if len(_objs) > 0:
			return _objs[0]
		else:
			return None
