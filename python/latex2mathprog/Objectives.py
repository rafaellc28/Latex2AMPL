class Objectives:
    """
    Class representing the node of the objective list in the AST of a MLP
    """
    
    def __init__(self, objectives):
        """
        Set the objective list
        
        :param Objectives : [Objective]
        """
        self.objectives = objectives
    
    def __str__(self):
        """
        to string
        """
        res = ""
        return "\nObj List:\n[" + "\n".join(map(lambda el: str(el), self.objectives)) + "]\n"
    
    def __len__(self):
        """
        length method
        """
        return len(self.objectives)

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.objectives)-1:
            self.i += 1         
            return self.objectives[self.i]
        else:
            self.i = -1
            raise StopIteration
    
    def getObjectives(self):
        """
        get the objectives
        """
        return self.objectives

    def addObjective(self, objective):
        """
        Add a objective to the list
        """
        self.objectives += [objective]
        return self

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this objective list
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for this objective list
        """
        return codeGenerator.generateCode(self)

class Objective:
    """
    Class representing the node of the objective function in the AST of a MLP
    """
    
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"
    
    def __init__(self, linearExpression, type = MINIMIZE, domain = None):
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
        Generate the MathProg code for the identifiers and sets used in this objective function
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for this Objective
        """
        return codeGenerator.generateCode(self)
