from GenObj import *

class GenType(GenObj):
	def __init__(self, name, varType = None):
		super(GenType, self).__init__(name)
		self.varType = varType

	def getVarType(self):
		return self.varType

	def setVarType(self, varType):
		self.varType = varType
