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
