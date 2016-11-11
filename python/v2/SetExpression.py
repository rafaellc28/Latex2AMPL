from Expression import *
from Variable import *
from ValueList import *

class SetExpression(Expression):
    """
    Class representing a set in the AST of the MLP
    """

class SetExpressionWithValue(SetExpression):
    """
    Class representing a set with value in the AST of the MLP
    """

    def __init__(self, value, dimension = 1):
        """
        Set the value that correspond to the Set expression
        
        :param value : Variable | ValueList | Range
        """

        self.value = value
        self.dimension = dimension
    
    def __str__(self):
        """
        to string
        """
        if isinstance(self.value, ValueList):
            return "SEV: {" + str(self.value) + "}"
        else:
            return "SEV: "+str(self.value)

    def setDimension(self, dimension):
        self.dimension = dimension

        if isinstance(self.value, Variable):
            self.value.setDimenSet(dimension)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Set expression
        """
        return codeGenerator.generateCode(self)


class SetExpressionWithIndices(SetExpression):
    """
    Class representing a set with indices in the AST of the MLP
    """

    def __init__(self, variable, indices, dimension = 0):
        """
        Set the value that correspond to the Set expression
        
        :param variable : Variable
        :param indices: ValueList | Variable
        """

        self.variable = variable
        self.indices = indices
        self.dimension = dimension

    def __str__(self):
        """
        to string
        """

        #if isinstance(self.indices, Variable):
        #    return "SEI: " + str(self.variable) + "[" + str(self.indices) + "]"
        #else:
        #    return "SEI: " + str(self.variable) + "[" + ",".join(map(lambda ind: str(ind), self.indices)) + "]"
        return "SEI: " + str(self.variable)

    def setDimension(self, dimension):
        self.dimension = dimension
        self.variable.setDimenSet(dimension)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Set expression
        """
        return codeGenerator.generateCode(self)


class SetExpressionWithOperation(SetExpression):
    """
    Class representing a set with operation in the AST of the MLP
    """

    DIFF    = "diff"
    SYMDIFF = "symdiff"
    UNION   = "union"
    INTER   = "inter"
    CROSS   = "cross"

    def __init__(self, op, setExpression1, setExpression2):
        """
        Set the operator and the expressions
        """
        
        self.op             = op
        self.setExpression1 = setExpression1
        self.setExpression2 = setExpression2

    def __str__(self):
        """
        to string
        """

        return "SETOP: " + str(self.setExpression1) + " " + self.op + " " + str(self.setExpression2)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Set expression
        """
        return codeGenerator.generateCode(self)
