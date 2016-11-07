from GenSubIndices import *

class GenObjWithSubIndices(object):
	def __init__(self, name):
		self.name = name
		self.sub_indices = GenSubIndices()
	
	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def getSubIndices(self):
		return self.sub_indices

	def setSubIndices(self, sub_indices):
		self.sub_indices = sub_indices
