# Abstract Syntax Tree (AST) for Latex (Mixed) Linear Progamming formulation (MLP)
class LinearProgram:
    """
    Class representing the root node in the AST of a MLP
    """

    def __init__(self, objective, constraints, declarations = None):
        """
        Set the objective and the constraints
        
        :param objective: Objective
        :param constraints: Constraints
        :param declarations: Declarations
        """
        
        self.objective = objective
        self.constraints = constraints
        self.declarations = declarations
    
    def __str__(self):
        """
        to string
        """
        res = "\nLP:\n" + str(self.objective) + "\n"
        
        if self.constraints:
            res += str(self.constraints) + "\n"
        
        if self.declarations:
            res += str(self.declarations) + "\n"
        
        return res
    
    def setDeclarations(self, declarations):
        self.declarations = declarations

    def setupEnvironment(self, codeSetup):
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for this Linear Program
        """
        return codeGenerator.generateCode(self)
