from SetExpression import *

class CircularSet(SetExpression):
    def __init__(self):
        SetExpression.__init__(self)

    def getSymbolName(self, codeGenerator):
        return self.generateCode(codeGenerator)

    def getDependencies(self, codeGenerator):
        return []

    def setupEnvironment(self, codeSetup):
        """
        Setup environment
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this Set
        """
        return codeGenerator.generateCode(self)
