# Abstract Syntax Tree (AST) for Latex (Mixed) Linear Progamming formulation (MLP)
class LinearProgram:
    """
    Class representing the root node in the AST of a MLP
    """

    def __init__(self, objectives, constraints, declarations = None):
        """
        Set the objective and the constraints
        
        :param objectives: Objectives
        :param constraints: Constraints
        """
        
        self.objectives = objectives
        self.constraints = constraints
        self.declarations = declarations
    
    def __str__(self):
        """
        to string
        """
        res = "\nLP:\n" + str(self.objectives) + "\n"
        
        if self.constraints:
            res += str(self.constraints) + "\n"
        
        return res
    
    def setupEnvironment(self, codeSetup):
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for this Linear Program
        """
        return codeGenerator.generateCode(self)
