from Expression import *

class ToComeExpression(Expression):
    """
    Class representing a to_come expression node in the AST of a MLP
    """
    TOCOME = "to_come"

    def __str__(self):
        """
        to string
        """
        return ToComeExpression.TOCOME

    def getDependencies(self, codeGenerator):
        return []

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for declaration of identifiers and sets in this to_come expression
        """
        codeSetup.setupEnvironment(self)
        
    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this to_come expression
        """
        return codeGenerator.generateCode(self)
