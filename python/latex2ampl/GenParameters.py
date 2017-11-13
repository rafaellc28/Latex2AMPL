from GenList import *

class GenParameters(GenList):
	def __init__(self):
		super(GenParameters, self).__init__()

	def getByNameAndStmtInclusion(self, name, stmtIndex):
		_params = filter(lambda el: el.getName() == name and el.getStmtInclusion() == str(stmtIndex), self.getAll())
		return _params
