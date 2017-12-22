from SetExpression import *
from Number import *
from Utils import *

class RealSet(SetExpression):
    def __init__(self, firstBound, firstOp, secondBound, secondOp):
        SetExpression.__init__(self)
        
        self.firstBound = firstBound
        self.firstOp = firstOp
        self.secondBound = secondBound
        self.secondOp = secondOp
        
    def setFirstBound(self, firstBound):
        self.firstBound = firstBound
        
    def getFirstBound(self):
        return self.firstBound
        
    def setFirstOp(self, firstOp):
        self.firstOp = firstOp
        
    def getFirstOp(self):
        return self.firstOp
        
    def setSecondBound(self, secondBound):
        self.secondBound = secondBound
        
    def getSecondBound(self):
        return self.secondBound
        
    def setSecondOp(self, secondOp):
        self.secondOp = secondOp
        
    def getSecondOp(self):
        return self.secondOp
        
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
        Generate the AMPL code for this Number
        """
        return codeGenerator.generateCode(self)
