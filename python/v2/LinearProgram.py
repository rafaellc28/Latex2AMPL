# Abstract Syntax Tree (AST) for Latex (Mixed) Linear Progamming formulation (MLP)
class LinearProgram:
    """
    Class representing the root node in the AST of a MLP
    """

    def __init__(self, objective, constraints):
        """
        Set the objective and the constraints
        
        :param objective: Objective
        :param constraints: Constraints
        """
        
        self.objective = objective
        self.constraints = constraints
    
    def __str__(self):
        """
        to string
        """
        
        if self.constraints:
            return "\nLP:\n" + str(self.objective) + "\n" + str(self.constraints) + "\n"
        else:
            return "\nLP:\n" + str(self.objective) + "\n"

    def setupEnvironment(self, codeSetup):
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for this Linear Program
        """
        return codeGenerator.generateCode(self)
