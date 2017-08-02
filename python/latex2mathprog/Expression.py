class Expression:
    """
    Class representing a expression node in the AST of a MLP
    """
    def __init__(self):
	    self.indice = -1
	    self.varName = None
	    self.varList = None

    def getSymbol(self):
        return self

    def getSymbolName(self, codeGenerator):
        return self.generateCode(codeGenerator)

    def getDimension(self):
        return 1

    def getIndice(self):
    	return self.indice

    def setIndice(self, indice):
    	self.indice = indice

    def getVarName(self):
    	return self.varName

    def setVarName(self, varName):
    	self.varName = varName

    def getVarList(self):
    	return self.varList

    def setVarList(self, varList):
    	self.varList = varList
