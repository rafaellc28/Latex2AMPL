from GenObjWithSubIndices import *

class GenSubIndicesByName(GenObjWithSubIndices):
	def __init__(self, name, firstStmt = None, lastStmt = None):
		super(GenSubIndicesByName, self).__init__(name, firstStmt, lastStmt)
