from GenObjWithSubIndices import *

class GenParameter(GenObjWithSubIndices):
	def __init__(self, name, constraintIndice = None):
		super(GenParameter, self).__init__(name)
		self.constraintIndice = constraintIndice
	
	def getConstraintIndice(self):
		return self.constraintIndice

	def setConstraintIndice(self, constraintIndice):
		self.constraintIndice = constraintIndice
