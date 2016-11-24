from Expression import *

class SymbolicExpression(Expression):
    """
    Class representing a numeric expression node in the AST of a MLP
    """

class SymbolicExpressionWithFunction(SymbolicExpression):
    """
    Class representing a numeric expression with function node in the AST of a MLP
    """

    SUBSTR   = "substr"
    TIME2STR = "time2str"

    def __init__(self, function, symbolicExpression, numericExpression1 = None, numericExpression2 = None):
        """
        Set the symbolic expression and the function
        
        :param function           : (substr | time2str)
        :param symbolicExpression : SymbolicExpression
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """

        self.function = function
        self.symbolicExpression = symbolicExpression
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2

    def __str__(self):
        """
        to string
        """

        res = str(self.function) + "("
        if self.function == SUBSTR:
            res += str(self.symbolicExpression) + "," + str(self.numericExpression1)
            if self.numericExpression2 != None:
                res += "," + str(self.numericExpression2)
        
        elif self.functiom == TIME2STR:
            res += str(self.numericExpression1) + "," + str(self.symbolicExpression)

        res += ")"

        return res

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this symbolic expression with function
        """
        return codeGenerator.generateCode(self)
    

class StringSymbolicExpression(SymbolicExpression):
    """
    Class representing a string symbolic expression node in the AST of a MLP
    """

    def __init__(self, value):
        """
        Set the single value of this symbolic expression

        :param value : String
        """

        self.value = value

    def __str__(self):
        """
        to string
        """
        
        return "StringSymbExpr:" + str(self.value)

    def __len__(self):
        """
        length method
        """

        return 1

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the string used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this string symbolic expression
        """
        return codeGenerator.generateCode(self)


class SymbolicExpressionBetweenParenthesis(SymbolicExpression):
    """
    Class representing a numeric expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, symbolicExpression):
        """
        Set the symbolic expression

        :param symbolicExpression : SymbolicExpression
        """

        self.symbolicExpression = symbolicExpression

    def __str__(self):
        """
        to string
        """
        
        return "SE: (" + str(self.symbolicExpression) + ")"
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this symbolic expression
        """
        return codeGenerator.generateCode(self)


class SymbolicExpressionWithOperation(SymbolicExpression):
    """
    Class representing a symbolic expression with operation node in the AST of a MLP
    """
    
    CONCAT  = "&"

    def __init__(self, op, symbolicExpression1, symbolicExpression2):
        """
        Set the expressions participating in the operation
        
        :param op                 : (CONCAT)
        :param symbolicExpression1 : SymbolicExpression
        :param symbolicExpression2 : SymbolicExpression
        """
        
        self.op                  = op
        self.symbolicExpression1 = symbolicExpression1
        self.symbolicExpression2 = symbolicExpression2
    
    def __str__(self):
        """
        to string
        """
        
        return "OpSE:" + str(self.symbolicExpression1) + " " + self.op + " " + str(self.symbolicExpression2)
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this symbolic expression with operation
        """
        return codeGenerator.generateCode(self)
