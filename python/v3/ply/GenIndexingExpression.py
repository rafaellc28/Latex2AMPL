from GenObj import *

class GenIndexingExpression(GenObj):
	def __init__(self, name, value):
		super(GenIndexingExpression, self).__init__(name)
		self.value = value

	def getValue(self):
		return self.value

	def setValue(self, value):
		self.value = value
