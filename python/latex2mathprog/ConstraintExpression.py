from Expression import *

class ConstraintExpression(Expression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """
    EQ = "="
    LE = "<="
    GE = ">="


class ConstraintExpression2(ConstraintExpression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """

    def __init__(self, linearExpression1, linearExpression2, op = ConstraintExpression.LE):
        """
        Set the expressions being related
        
        :param linearExpression1: LinearExpression
        :param linearExpression2: LinearExpression
        """
        
        self.linearExpression1 = linearExpression1
        self.linearExpression2 = linearExpression2
        self.op = op
        
    def __str__(self):
        """
        to string
        """
        
        return "CntExprWith2:" + str(self.linearExpression1) + " " + self.op + " " + str(self.linearExpression2)

    def getDependencies(self, codeGenerator):
        return list(set(self.linearExpression1.getDependencies(codeGenerator) + self.linearExpression2.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets in this constraint
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this constraint expression
        """
        return codeGenerator.generateCode(self)


class ConstraintExpression3(ConstraintExpression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """

    def __init__(self, linearExpression, numericExpression1, numericExpression2, op = ConstraintExpression.LE):
        """
        Set the expressions being related
        
        :param linearExpression   : LinearExpression
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """
        
        self.linearExpression   = linearExpression
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
        self.op = op
        
    def __str__(self):
        """
        to string
        """
        
        return "CntExprWith3:" + str(self.numericExpression1) + " " + self.op + " " + str(self.linearExpression) + " " + self.op + " " + str(self.numericExpression2)
    
    def getDependencies(self, codeGenerator):
        return list(set(self.linearExpression.getDependencies(codeGenerator) + self.numericExpression1.getDependencies(codeGenerator) + self.numericExpression2.getDependencies(codeGenerator)))
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets in this constraint
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this constraint expression
        """
        return codeGenerator.generateCode(self)
