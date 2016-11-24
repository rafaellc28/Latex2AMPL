from Expression import *

class Range(Expression):
    """
    Class representing a range in the AST of the MLP
    """
    
    def __init__(self, rangeInit, rangeEnd):
        """
        Set the range init and end
        
        :param rangeInit : NumericExpression
        :param rangeEnd  : NumericExpression
        """
        
        self.rangeInit = rangeInit
        self.rangeEnd  = rangeEnd

    def __str__(self):
        """
        to string
        """
        
        return "Range: [" + str(self.rangeInit) + ".." + str(self.rangeEnd) + "]"

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Range
        """
        return codeGenerator.generateCode(self)
