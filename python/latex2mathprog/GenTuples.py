from GenList import *

class GenTuples(GenList):
	def __init__(self):
		super(GenTuples, self).__init__()

	def get(self, obj):
		objVal = self.getObjVal(obj)
		if objVal == None:
			return None

		_objs = filter(lambda el: el.getName() == objVal and el.getTupleVal() == obj.getTupleVal() and el.getStmtIndex() == obj.getStmtIndex(), self.vector)

		if len(_objs) > 0:
			return _objs[0]
		else:
			return None
