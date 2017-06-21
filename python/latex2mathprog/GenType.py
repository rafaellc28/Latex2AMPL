from GenObj import *

class GenType(GenObj):
	def __init__(self, name, _type = None, minVal = None, maxVal = None):
		super(GenType, self).__init__(name)
		self.type = _type
		self.minVal = minVal
		self.maxVal = maxVal
	
	def getType(self):
		return self.type

	def setType(self, _type):
		self.type = _type

	def getMinVal(self):
		return self.minVal

	def setMinVal(self, minVal):
		if self.minVal == None or minVal < self.minVal:
			self.minVal = minVal

	def getMaxVal(self):
		return self.maxVal

	def setMaxVal(self, maxVal):
		if self.maxVal == None or maxVal > self.maxVal:
			self.maxVal = minVal
