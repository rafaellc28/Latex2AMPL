from Expression import *

class LinearExpression(Expression):
    """
    Class representing a linear expression node in the AST of a MLP
    """

class ValuedLinearExpression(LinearExpression):
    """
    Class representing a valued linear expression node in the AST of a MLP
    """

    def __init__(self, value):
        """
        Set the single value of this linear expression

        :param value : Identifier | Number
        """

        self.value = value

    def __str__(self):
        """
        to string
        """
        
        return "ValuedExpr:" + str(self.value)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of identifiers and sets in this linear expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this valued linear expression
        """
        return codeGenerator.generateCode(self)


class LinearExpressionBetweenParenthesis(LinearExpression):
    """
    Class representing a linear expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, linearExpression):
        """
        Set the linear expression

        :param linearExpression : LinearExpression
        """

        self.linearExpression = linearExpression

    def __str__(self):
        """
        to string
        """
        
        return "LE: (" + str(self.linearExpression) + ")"

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of identifiers and sets in this linear expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this linear expression
        """
        return codeGenerator.generateCode(self)


class LinearExpressionWithArithmeticOperation(LinearExpression):
    """
    Class representing a linear expression with arithmetic operation node in the AST of a MLP
    """
    
    PLUS  = "+"
    MINUS = "-"
    TIMES = "*"
    DIV   = "/"

    def __init__(self, op, expression1, expression2):
        """
        Set the expressions participating in the arithmetic operation
        
        :param op          : (PLUS, MINUS, TIMES, DIV)
        :param expression1 : LinearExpression | NumericExpression
        :param expression2 : LinearExpression | NumericExpression
        """
        
        self.op          = op
        self.expression1 = expression1
        self.expression2 = expression2
    
    def __str__(self):
        """
        to string
        """
        
        return "OpLE:" + str(self.expression1) + " " + self.op + " " + str(self.expression2)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of identifiers and sets in this linear expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this linear expression with arithmetic pperation
        """
        return codeGenerator.generateCode(self)


class MinusLinearExpression(LinearExpression):
    """
    Class representing a minus linear expression node in the AST of a MLP
    """
    
    def __init__(self, linearExpression):
        """
        Set the expressions being negated
        
        :param linearExpression: LinearExpression
        """
        
        self.linearExpression = linearExpression
    
    def __str__(self):
        """
        to string
        """
        
        return "MinusLE:" + "-(" + str(self.linearExpression) + ")"
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of identifiers and sets in this linear expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this minus linear expression
        """
        return codeGenerator.generateCode(self)


class IteratedLinearExpression(LinearExpression):
    """
    Class representing a iterated linear expression node in the AST of a MLP
    """
    
    def __init__(self, linearExpression, indexingExpression, numericExpression = None):
        """
        Set the components of the iterated linear expression

        :param linearExpression   : LinearExpression
        :param indexingExpression : IndexingExpression
        :param numericExpression  : NumericExpression
        """
        
        self.linearExpression   = linearExpression
        self.indexingExpression = indexingExpression
        self.numericExpression  = numericExpression

    def __str__(self):
        """
        to string
        """
        
        res = "sum(" + str(self.indexingExpression) + ")"

        if self.numericExpression:
            res += "^(" + str(self.numericExpression) + ")"

        res += "(" + str(self.linearExpression) + ")"

        return "ItLE:" + res
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of identifiers and sets in this linear expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this iterated linear expression
        """
        return codeGenerator.generateCode(self)

class ConditionalLinearExpression(LinearExpression):
    """
    Class representing a conditional linear expression node in the AST of a MLP
    """
    
    def __init__(self, logicalExpression, linearExpression1, linearExpression2 = None):
        """
        Set the conditional linear expression
        
        :param logicalExpression : LogicalExpression
        :param linearExpression1 : LinearExpression
        :param linearExpression2 : LinearExpression
        """
        
        self.logicalExpression = logicalExpression
        self.linearExpression1 = linearExpression1
        self.linearExpression2 = linearExpression2
    
    def __str__(self):
        """
        to string
        """
        res = "CondLinearExpr: " + "("+str(self.logicalExpression)+")?" + str(self.linearExpression1)

        if self.linearExpression2 != None:
            res += ": " + str(self.linearExpression2)

        return res
    
    def addElseExpression(self, elseExpression):
        self.linearExpression2 = elseExpression

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this conditional linear expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this contitional linear expression
        """
        return codeGenerator.generateCode(self)
