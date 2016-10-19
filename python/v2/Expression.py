class Expression:
    """
    Class representing a expression node in the AST of a MLP
    """
    def __init__(self):
	    self.indice = -1

    def getIndice(self):
    	return self.indice

    def setIndice(self, indice):
    	self.indice = indice
