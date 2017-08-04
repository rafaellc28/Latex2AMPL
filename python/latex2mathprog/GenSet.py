from GenObj import *

class GenSet(GenObj):
	def __init__(self, name, dimen = 1, certainty = True, isDeclaredAsSet = False):
		super(GenSet, self).__init__(name)
		self.dimen = dimen
		self.certainty = certainty
		self.isDeclaredAsSet = isDeclaredAsSet
	
	def getDimension(self):
		return self.dimen

	def setDimension(self, dimen):
		self.dimen = dimen

	def getCertainty(self):
		return self.certainty

	def setCertainty(self, certainty):
		self.certainty = certainty

	def getIsDeclaredAsSet(self):
		return self.isDeclaredAsSet

	def setIsDeclaredAsSet(self, isDeclaredAsSet):
		self.isDeclaredAsSet = isDeclaredAsSet
