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

    ABS         = "abs"
    ATAN        = "atan"
    ATAN2       = "atan2"
    ATANH       = "atanh"
    TAN         = "tan"
    TANH        = "tanh"
    CARD        = "card"
    CEIL        = "ceil"
    COS         = "cos"
    ACOS        = "acos"
    COSH        = "cosh"
    ACOSH       = "acosh"
    FLOOR       = "floor"
    EXP         = "exp"
    LENGTH      = "length"
    LOG         = "log"
    LOG10       = "log10"
    ROUND       = "round"
    PRECISION   = "precision"
    SIN         = "sin"
    ASIN        = "asin"
    SINH        = "sinh"
    ASINH       = "asinh"
    SQRT        = "sqrt"
    TRUNC       = "trunc"
    MIN         = "min"
    MAX         = "max"
    STR2TIME    = "str2time"
    GMTIME      = "gmtime"
    TIME        = "time"
    UNIFORM01   = "Uniform01"
    UNIFORM     = "Uniform"
    NORMAL01    = "Normal01"
    NORMAL      = "Normal"
    BETA        = "Beta"
    IRAND224    = "Irand224"
    CAUCHY      = "Cauchy"
    EXPONENTIAL = "Exponential"
    GAMMA       = "Gamma"
    POISSON     = "Poisson"
    NUM         = "num"
    NUM0        = "num0"
    ICHAR       = "ichar"
    MATCH       = "match"

    def __init__(self, function, numericExpression1 = None, numericExpression2 = None):
        """
        Set the numeric expression and the function

        :param function           : (abs | atan | card | ceil | cos | floor | exp | length | log | log10 | round | sin | sqrt | trunc | gmtime | time)
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
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this numeric expression with function
        """
        return codeGenerator.generateCode(self)
    


class FractionalNumericExpression(NumericExpression):
    """
    Class representing a fractional numeric expression node in the AST of a MLP
    """

    def __init__(self, numerator, denominator):
        """
        Set the single value of this numeric expression

        :param numerator   : Identifier | NumericExpression
        :param denominator : Identifier | NumericExpression
        """

        NumericExpression.__init__(self)

        self.numerator   = numerator
        self.denominator = denominator

    def __str__(self):
        """
        to string
        """
        return "FractionalNumericExpression: " + str(self.numerator) + "/"+str(self.denominator)

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

    def getDependencies(self, codeGenerator):
        dep = []

        if self.numerator != None:
            dep += self.numerator.getDependencies(codeGenerator)

        if self.denominator != None:
            dep += self.denominator.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the identifiers and sets used in this fractional numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this fractional numeric expression
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

    def getValue(self):
        return self.value

    def getSymbol(self):
        return self.value

    def getDependencies(self, codeGenerator):
        return self.value.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the identifiers and sets used in this valued numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this valued numeric expression
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
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this numeric expression
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
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this numeric expression with arithmetic operation
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
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this minus numeric expression
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
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this iterated numeric expression
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
        res = "CondNumExpr: " + " IF "+str(self.logicalExpression)+" THEN " + str(self.numericExpression1)

        if self.numericExpression2 != None:
            res += " ELSE " + str(self.numericExpression2)

        res += " ENDIF "

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
        Generate the AMPL code for the identifiers and sets used in this conditional numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this conditional numeric expression
        """
        return codeGenerator.generateCode(self)


class IteratedNumericExpression2(NumericExpression):
    """
    Class representing a Iterated Numeric Expression expression node in the AST of a MLP
    """
    
    COUNT    = "count"
    ATMOST   = "atmost"
    ATLEAST  = "atleast"
    EXACTLY  = "exactly"
    NUMBEROF = "numberof"

    def __init__(self, op, constraintExpression, indexingExpression, numericExpression = None):
        """
        Set the components of the iterated numeric expression
        
        :param op                   : COUNT | ATMOST | ATLEAST | EXACTLY | NUMBEROF
        :param constraintExpression : ConstraintExpression
        :param indexingExpression   : IndexingExpression
        :param numericExpression    : NumericExpression
        """

        self.op = op
        self.constraintExpression = constraintExpression
        self.indexingExpression   = indexingExpression
        self.numericExpression    = numericExpression

    def __str__(self):
        """
        to string
        """
        res = self.op
        if self.numericExpression:
            res += " " + str(self.numericExpression)

        if self.op == IteratedNumericExpression2.NUMBEROF:
            res += " in ({"+ str(self.indexingExpression) +"} " + str(self.constraintExpression) + ")"

        else:
            res += " {"+ str(self.indexingExpression) +"} " + str(self.constraintExpression)

        return "ItConstraintExpression: " + res

    def getDependencies(self, codeGenerator):
        dep = self.constraintExpression.getDependencies(codeGenerator) + self.indexingExpression.getDependencies(codeGenerator)

        if self.numericExpression != None:
            dep += self.numericExpression.getDependencies(codeGenerator)

        return list(set(dep))
        
    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this linear expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this iterated linear expression
        """
        return codeGenerator.generateCode(self)


class PiecewiseItemExpression(NumericExpression):
    """
    Class representing a Piecewise Item Expression expression node in the AST of a MLP
    """
    
    def __init__(self, itemExpression, indexingExpression = None):
        """
        Set the components of the piecewise item expression
        
        :param itemExpression       : Identifier | NumericSymbolicExpression
        :param indexingExpression   : IndexingExpression
        """

        self.itemExpression       = itemExpression
        self.indexingExpression   = indexingExpression

    def __str__(self):
        """
        to string
        """
        
        res = str(self.itemExpression)

        if self.indexingExpression:
            res += " for " + str(self.indexingExpression)

        return "PiecewiseItemExpression: " + res

    def getDependencies(self, codeGenerator):
        dep = self.itemExpression.getDependencies(codeGenerator)

        if self.indexingExpression != None:
            dep += self.indexingExpression.getDependencies(codeGenerator)

        return list(set(dep))
        
    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this piecewise item expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this piecewise item expression
        """
        return codeGenerator.generateCode(self)

class PiecewiseExpression(NumericExpression):
    """
    Class representing a Piecewise Expression expression node in the AST of a MLP
    """
    
    def __init__(self, breakpointList, slopeList, argumentExpression = None, zeroExpression = None):
        """
        Set the components of the piecewise expression
        
        :param breakpointList     : [PiecewiseItemExpression]
        :param slopeList          : [PiecewiseItemExpression]
        :param argumentExpression : Identifier | NumericSymbolicExpression
        :param zeroExpression     : Identifier | NumericSymbolicExpression
        """

        self.breakpointList     = breakpointList
        self.slopeList          = slopeList
        self.argumentExpression = argumentExpression
        self.zeroExpression     = zeroExpression

    def __str__(self):
        """
        to string
        """
        
        res = "<<" + ", ".join(map(lambda el: str(el), self.breakpointList)) + "; " + ", ".join(map(lambda el: str(el), self.slopeList)) + ">>"

        if self.argumentExpression:
            res += " " + str(self.argumentExpression)

        if self.zeroExpression:
            res += " " + str(self.zeroExpression)

        return "PiecewiseExpression: " + res

    def setArgumentExpression(self, argumentExpression):
        self.argumentExpression = argumentExpression

    def setZeroExpression(self, zeroExpression):
        self.zeroExpression = zeroExpression

    def getDependencies(self, codeGenerator):
        dep = map(lambda el: el.getDependencies(codeGenerator), self.breakpointList) + map(lambda el: el.getDependencies(codeGenerator), self.slopeList)

        if self.argumentExpression != None:
            dep += self.argumentExpression.getDependencies(codeGenerator)

        if self.zeroExpression != None:
            dep += self.zeroExpression.getDependencies(codeGenerator)

        return list(set(dep))
        
    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this piecewise expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this piecewise xpression
        """
        return codeGenerator.generateCode(self)
