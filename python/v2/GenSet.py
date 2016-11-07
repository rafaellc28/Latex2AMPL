from GenObjWithSubIndices import *

class GenSet(GenObjWithSubIndices):
	def __init__(self, name, dimen = 1):
		super(GenSet, self).__init__(name)
		self.dimen = dimen

	def getDimension(self):
		return self.dimen

	def setDimension(self, dimen):
		self.dimen = dimen
