from Expression import *

class NumericExpression(Expression):
    """
    Class representing a numeric expression node in the AST of a MLP
    """
    def __init__(self):
        Expression.__init__(self)

class NumericExpressionWithFunction(NumericExpression):
    """
    Class representing a numeric expression with function node in the AST of a MLP
    """

    ABS       = "abs"
    ATAN      = "atan"
    CARD      = "card"
    CEIL      = "ceil"
    COS       = "cos"
    FLOOR     = "floor"
    EXP       = "exp"
    LENGTH    = "length"
    LOG       = "log"
    LOG10     = "log10"
    ROUND     = "round"
    SIN       = "sin"
    SQRT      = "sqrt"
    TRUNC     = "trunc"
    MIN       = "min"
    MAX       = "max"
    STR2TIME  = "str2time"
    GMTIME    = "gmtime"
    UNIFORM01 = "Uniform01"
    UNIFORM   = "Uniform"
    NORMAL01  = "Normal01"
    NORMAL    = "Normal"
    IRAND224  = "Irand224"

    def __init__(self, function, numericExpression1 = None, numericExpression2 = None):
        """
        Set the numeric expression and the function

        :param function           : (abs | atan | card | ceil | cos | floor | exp | length | log | log10 | round | sin | sqrt | trunc | gmtime)
        :param numericExpression  : NumericExpression | SymbolicExpression | ValueList
        :param numericExpression2 : NumericExpression | SymbolicExpression
        """

        NumericExpression.__init__(self)

        self.function = function
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2

    def __str__(self):
        """
        to string
        """
        res = str(self.function) + "("

        if self.numericExpression1 != None:
            res += str(self.numericExpression1)

        if self.numericExpression2 != None:
            res += ", " + str(self.numericExpression2)

        res += ")"
        
        return res

    def getDependencies(self, codeGenerator):
        dep = []

        if self.numericExpression1 != None:
            dep += self.numericExpression1.getDependencies(codeGenerator)

        if self.numericExpression2 != None:
            dep += self.numericExpression2.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this numeric expression with function
        """
        return codeGenerator.generateCode(self)
    

class ValuedNumericExpression(NumericExpression):
    """
    Class representing a valued numeric expression node in the AST of a MLP
    """

    def __init__(self, value):
        """
        Set the single value of this numeric expression

        :param value : Identifier | Number
        """

        NumericExpression.__init__(self)

        self.value = value

    def __str__(self):
        """
        to string
        """
        
        return "ValuedNumExpr:" + str(self.value)

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

    def getSymbol(self):
        return self.value

    def getDependencies(self, codeGenerator):
        return self.value.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this valued linear expression
        """
        return codeGenerator.generateCode(self)


class NumericExpressionBetweenParenthesis(NumericExpression):
    """
    Class representing a numeric expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, numericExpression):
        """
        Set the numeric expression

        :param numericExpression : NumericExpression
        """

        NumericExpression.__init__(self)

        self.numericExpression = numericExpression

    def __str__(self):
        """
        to string
        """
        
        return "NEBetweenParenthesis: (" + str(self.numericExpression) + ")"

    def getDependencies(self, codeGenerator):
        return self.numericExpression.getDependencies(codeGenerator)
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this numeric expression
        """
        return codeGenerator.generateCode(self)


class NumericExpressionWithArithmeticOperation(NumericExpression):
    """
    Class representing a numeric expression with arithmetic operation node in the AST of a MLP
    """
    
    PLUS  = "+"
    MINUS = "-"
    TIMES = "*"
    DIV   = "/"
    MOD   = "mod"
    POW   = "^"
    QUOT  = "div"
    LESS  = "less"

    def __init__(self, op, numericExpression1, numericExpression2):
        """
        Set the expressions participating in the arithmetic operation
        
        :param op                 : (PLUS, MINUS, TIMES, MOD, POW)
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """

        NumericExpression.__init__(self)
        
        self.op                 = op
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
    
    def __str__(self):
        """
        to string
        """
        res = "OpArthNE:" + str(self.numericExpression1) + " " + self.op + " "
        if self.op == NumericExpressionWithArithmeticOperation.POW and not (isinstance(self.numericExpression2, ValuedNumericExpression) or isinstance(self.numericExpression2, NumericExpressionBetweenParenthesis)):
            res += "{" + str(self.numericExpression2) + "}"
        else:
            res += str(self.numericExpression2)

        return res

    def getDependencies(self, codeGenerator):
        return list(set(self.numericExpression1.getDependencies(codeGenerator) + self.numericExpression2.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this numeric expression with arithmetic operation
        """
        return codeGenerator.generateCode(self)


class MinusNumericExpression(NumericExpression):
    """
    Class representing a minus numeric expression node in the AST of a MLP
    """
    
    def __init__(self, numericExpression):
        """
        Set the numeric expression being negated
        
        :param numericExpression: NumericExpression
        """

        NumericExpression.__init__(self)
        
        self.numericExpression = numericExpression
    
    def __str__(self):
        """
        to string
        """
        
        return "MinusNE:" + "-(" + str(self.numericExpression) + ")"

    def getDependencies(self, codeGenerator):
        return self.numericExpression.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this minus numeric expression
        """
        return codeGenerator.generateCode(self)


class IteratedNumericExpression(NumericExpression):
    """
    Class representing a iterated numeric expression node in the AST of a MLP
    """

    SUM  = "sum"
    PROD = "prod"
    MAX  = "max"
    MIN  = "min"

    def __init__(self, op, numericExpression, indexingExpression, supNumericExpression = None):
        """
        Set the components of the iterated linear expression

        :param op                   : op
        :param numericExpression    : NumericExpression
        :param indexingExpression   : IndexingExpression
        :param supNumericExpression : NumericExpression
        """

        NumericExpression.__init__(self)
        
        self.op                   = op
        self.numericExpression    = numericExpression
        self.indexingExpression   = indexingExpression
        self.supNumericExpression = supNumericExpression

    def __str__(self):
        """
        to string
        """
        
        res = str(self.op) + "(" + str(self.indexingExpression) + ")"

        if self.supNumericExpression:
            res += "^" + str(self.supNumericExpression)

        res += str(self.numericExpression)

        return "ItNumExp:" + res + "|"

    def getDependencies(self, codeGenerator):
        dep = self.numericExpression.getDependencies(codeGenerator) + self.indexingExpression.getDependencies(codeGenerator)

        if self.supNumericExpression != None:
            dep += self.supNumericExpression.getDependencies(codeGenerator)

        return list(set(dep))
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this iterated numeric expression
        """
        return codeGenerator.generateCode(self)

class ConditionalNumericExpression(NumericExpression):
    """
    Class representing a conditional numeric expression node in the AST of a MLP
    """
    
    def __init__(self, logicalExpression, numericExpression1, numericExpression2 = None):
        """
        Set the conditional numeric expression
        
        :param logicalExpression : LogicalExpression
        :param numericExpression1: NumericExpression
        :param numericExpression2: NumericExpression
        """

        NumericExpression.__init__(self)
        
        self.logicalExpression  = logicalExpression
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
    
    def __str__(self):
        """
        to string
        """
        res = "CondNumExpr: " + "("+str(self.logicalExpression)+")?" + str(self.numericExpression1)

        if self.numericExpression2 != None:
            res += ": " + str(self.numericExpression2)

        return res

    def addElseExpression(self, elseExpression):
        self.numericExpression2 = elseExpression
    
    def getDependencies(self, codeGenerator):
        dep = self.logicalExpression.getDependencies(codeGenerator) + self.numericExpression1.getDependencies(codeGenerator)

        if self.numericExpression2 != None:
            dep += self.numericExpression2.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this conditional numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this conditional numeric expression
        """
        return codeGenerator.generateCode(self)
