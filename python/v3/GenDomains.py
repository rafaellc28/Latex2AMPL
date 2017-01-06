from GenList import *

class GenDomains(GenList):
	def __init__(self):
		super(GenDomains, self).__init__()

	def get(self, obj):
		objVal = self.getObjVal(obj)
		if objVal == None:
			return None

		_objs = filter(lambda el: el.getName() == objVal and el.getStmtIndex() == obj.getStmtIndex() and el.getOrder() == obj.getOrder(), self.vector)

		if len(_objs) > 0:
			return _objs[0]
		else:
			return None
	
	def getByNameAndStmt(self, name, stmtIndex):
		_domains = filter(lambda el: el.getName() == name and el.getStmtIndex() == stmtIndex, self.getAll())
		return _domains

	def getBiggestOrderByNameAndStmt(self, name, stmtIndex):
		_domains = self.getByNameAndStmt(name, stmtIndex)

		if len(_domains) == 0:
			return -1

		order = -1
		for _d in _domains:
			if _d.getOrder() > order:
				order = _d.getOrder()
		
		return order
