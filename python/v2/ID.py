from Expression import *

class ID(Expression):
    """
    Class representing a variable node in the AST of the MLP
    """
    
    def __init__(self, variable):
        """
        Set the string that represents the variable
        
        :param variable: String
        """

        Expression.__init__(self)
        
        self.variable = variable
    
    def __str__(self):
        """
        to string
        """
        
        return self.variable

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of this ID
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Variable
        """
        return codeGenerator.generateCode(self)
