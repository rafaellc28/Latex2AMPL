from Expression import *

class String(Expression):
    """
    Class representing a number node in the AST of the MLP
    """

    def __init__(self, string):
        """
        Set the string
        
        :param string: str
        """
        Expression.__init__(self)
        
        self.string = string
    
    def __str__(self):
        """
        to string
        """
        
        return str(self.string)

    def __len__(self):
        """
        length method
        """
        return 1

    def __iter__(self):
        """
        Get the iterator of the class
        """
        return [self]

    def getDependencies(self, codeGenerator):
        return []
    
    def setupEnvironment(self, codeSetup):
        """
        Setup environment
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Number
        """
        return codeGenerator.generateCode(self)