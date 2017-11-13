from GenObj import *

class GenVariable(GenObj):
	def __init__(self, name, _type = None, certainty = True, isDeclaredAsVar = False):
		super(GenVariable, self).__init__(name)
		self.type = _type
		self.certainty = certainty
		self.isDeclaredAsVar = isDeclaredAsVar
		
	def getType(self):
		return self.type

	def setType(self, _type):
		self.type = _type
	
	def getCertainty(self):
		return self.certainty

	def setCertainty(self, certainty):
		self.certainty = certainty

	def getIsDeclaredAsVar(self):
		return self.isDeclaredAsVar

	def setIsDeclaredAsVar(self, isDeclaredAsVar):
		self.isDeclaredAsVar = isDeclaredAsVar
