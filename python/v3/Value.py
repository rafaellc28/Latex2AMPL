from Expression import *

class Value(Expression):
    """
    Class representing an Value in the AST of the MLP
    """

    def __init__(self, value):
        """
        Set the value

        :param value: float|Variable
        """

        if isinstance(value, float):
            self.value = Number(value)
        else:
            self.value = value

    def __str__(self):
        """
        to string
        """

        return "Value: "  + str(self.value)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of the variable of this value
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Value
        """
        return codeGenerator.generateCode(self)
