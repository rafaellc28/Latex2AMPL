from GenObj import *

class GenTuple(GenObj):
	def __init__(self, name, tupleVal, op, stmtIndex, tupleObj = None):
		super(GenTuple, self).__init__(name)
		self.tupleVal = tupleVal
		self.op = op
		self.stmtIndex = stmtIndex
		self.tupleObj = tupleObj

	def getTupleVal(self):
		return self.tupleVal

	def setTupleVal(self, tupleVal):
		self.tupleVal = tupleVal

	def getOp(self):
		return self.op

	def setOp(self, op):
		self.op = op

	def getStmtIndex(self):
		return self.stmtIndex

	def setStmtIndex(self, stmtIndex):
		self.stmtIndex = stmtIndex

	def getTupleObj(self):
		return self.tupleObj

	def setTupleObj(self, tupleObj):
		self.tupleObj = tupleObj
