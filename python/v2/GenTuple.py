from GenObj import *

class GenTuple(GenObj):
	def __init__(self, name, tupleVal, op):
		super(GenTuple, self).__init__(name)
		self.tupleVal = tupleVal
		self.op = op

	def getTupleVal(self):
		return self.tupleVal

	def setTupleVal(self, tupleVal):
		self.tupleVal = tupleVal

	def getOp(self):
		return self.op

	def setOp(self, op):
		self.op = op
