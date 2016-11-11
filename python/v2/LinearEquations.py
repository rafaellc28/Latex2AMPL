# Abstract Syntax Tree (AST) for Latex Linear Equations
class LinearEquations:
    """
    Class representing the root node in the AST of a System of Linear Equations
    """

    def __init__(self, constraints):
        """
        Set the objective and the constraints
        
        :param constraints: Constraints
        """
        
        self.constraints = constraints
    
    def __str__(self):
        """
        to string
        """
        return "\nLEQ:\n" + str(self.constraints) + "\n"

    def setupEnvironment(self, codeSetup):
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for this Linear Program
        """
        return codeGenerator.generateCode(self)
