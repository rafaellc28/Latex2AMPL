from GenObjWithSubIndices import *

class GenSet(GenObjWithSubIndices):
	def __init__(self, name, dimen = 1, constraintIndice = None):
		super(GenSet, self).__init__(name)
		self.dimen = dimen
		self.constraintIndice = constraintIndice

	def getDimension(self):
		return self.dimen

	def setDimension(self, dimen):
		self.dimen = dimen
	
	def getConstraintIndice(self):
		return self.constraintIndice

	def setConstraintIndice(self, constraintIndice):
		self.constraintIndice = constraintIndice
