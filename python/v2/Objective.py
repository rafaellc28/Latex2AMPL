class Objective:
    """
    Class representing the node of the objective function in the AST of a MLP
    """
    
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"
    
    def __init__(self, linearExpression, type = MAXIMIZE, domain = None):
        """
        Set the objective type (maximize/minimize) and the expression being maximized/minimized
        
        :param linearExpression : LinearExpression
        :param type             : (MAXIMIZE,MINIMIZE)
        :param domain           : optional indexing expression
        """
        
        self.linearExpression = linearExpression
        self.type = type
        self.domain = domain
    
    def __str__(self):
        """
        to string
        """
        
        return "\nObj:\n" + str(self.type) + ": " + str(self.linearExpression) + "\n"
    
    def setDomain(domain):
        """
        Set the domain
        """

        self.domain = domain

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the variables and sets used in this objective function
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for this Objective
        """
        return codeGenerator.generateCode(self)
