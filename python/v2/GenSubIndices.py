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

		if len(_subIndices) > 0:
			return _subIndices[0]

		return None

	def getAllSortedByIndice(self):
		return self.getAllSortedByKey(lambda el: el.getIndice())

	def get(self, obj):
		objVal = self.getObjVal(obj)
		if objVal == None:
			return None

		_objs = filter(lambda el: el.getName() == objVal and el.getIndice() == obj.getIndice() and el.getStmtIndex() == obj.getStmtIndex(), self.vector)

		if len(_objs) > 0:
			return _objs[0]
		else:
			return None
