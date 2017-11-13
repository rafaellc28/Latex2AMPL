from Expression import *

class SymbolicExpression(Expression):
    """
    Class representing a numeric expression node in the AST of a MLP
    """
    def __init__(self):
        Expression.__init__(self)

class SymbolicExpressionWithFunction(SymbolicExpression):
    """
    Class representing a numeric expression with function node in the AST of a MLP
    """

    SUBSTR   = "substr"
    TIME2STR = "time2str"
    ALIAS    = "alias"
    CTIME    = "ctime"
    CHAR     = "char"
    SPRINTF  = "sprintf"
    SUB      = "sub"
    GSUB     = "gsub"

    def __init__(self, function, firstExpression = None, numericExpression1 = None, numericExpression2 = None):
        """
        Set the symbolic expression and the function
        
        :param function           : (substr | time2str | alias | ctime | char | sprintf)
        :param firstExpression    : SymbolicExpression | NumericExpression
        :param numericExpression1 : NumericExpression | ValueList
        :param numericExpression2 : NumericExpression
        """

        SymbolicExpression.__init__(self)

        self.function = function
        self.firstExpression    = firstExpression
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2

    def __str__(self):
        """
        to string
        """

        res = str(self.function) + "("
        if self.function == SymbolicExpressionWithFunction.SPRINTF:
            res += str(self.firstExpression) + "," + str(self.numericExpression1)

        elif self.function == SymbolicExpressionWithFunction.CTIME:
            if self.firstExpression != None:
                res += str(self.firstExpression)

        elif self.function == SymbolicExpressionWithFunction.ALIAS or self.function == SymbolicExpressionWithFunction.CHAR:
            res += str(self.firstExpression)

        elif self.function == SymbolicExpressionWithFunction.SUBSTR or self.function == SymbolicExpressionWithFunction.SUB or self.function == SymbolicExpressionWithFunction.GSUB:
            res += str(self.firstExpression) + "," + str(self.numericExpression1)
            if self.numericExpression2 != None:
                res += "," + str(self.numericExpression2)
            
        elif self.function == SymbolicExpressionWithFunction.TIME2STR:
            res += str(self.firstExpression) + "," + str(self.numericExpression1)

        res += ")"

        return res

    def getDependencies(self, codeGenerator):
        deps = []

        if self.firstExpression != None:
            deps += self.firstExpression.getDependencies(codeGenerator)

        if self.numericExpression1 != None:
            deps += self.numericExpression1.getDependencies(codeGenerator)

        if self.numericExpression2 != None:
            deps += self.numericExpression2.getDependencies(codeGenerator)

        return list(set(deps))

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this symbolic expression with function
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

        SymbolicExpression.__init__(self)

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

    def getSymbol(self):
        return self.value

    def getDependencies(self, codeGenerator):
        return self.value.getDependencies(codeGenerator)
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the string used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this string symbolic expression
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

        SymbolicExpression.__init__(self)

        self.symbolicExpression = symbolicExpression

    def __str__(self):
        """
        to string
        """
        
        return "SE: (" + str(self.symbolicExpression) + ")"
    
    def getDependencies(self, codeGenerator):
        return self.symbolicExpression.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this symbolic expression
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

        SymbolicExpression.__init__(self)
        
        self.op                  = op
        self.symbolicExpression1 = symbolicExpression1
        self.symbolicExpression2 = symbolicExpression2
    
    def __str__(self):
        """
        to string
        """
        
        return "OpSE:" + str(self.symbolicExpression1) + " " + self.op + " " + str(self.symbolicExpression2)

    def getDependencies(self, codeGenerator):
        return list(set(self.symbolicExpression1.getDependencies(codeGenerator) + self.symbolicExpression2.getDependencies(codeGenerator)))
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this symbolic expression with operation
        """
        return codeGenerator.generateCode(self)

class ConditionalSymbolicExpression(SymbolicExpression):
    """
    Class representing a conditional symbolic expression node in the AST of a MLP
    """
    
    def __init__(self, logicalExpression, symbolicExpression1, symbolicExpression2 = None):
        """
        Set the conditional symbolic expression
        
        :param logicalExpression  : LogicalExpression
        :param symbolicExpression1: SymbolicExpression
        :param symbolicExpression2: SymbolicExpression
        """

        SymbolicExpression.__init__(self)
        
        self.logicalExpression   = logicalExpression
        self.symbolicExpression1 = symbolicExpression1
        self.symbolicExpression2 = symbolicExpression2
    
    def __str__(self):
        """
        to string
        """
        res = "CondSymbExpr: " + "("+str(self.logicalExpression)+")?" + str(self.symbolicExpression1)

        if self.symbolicExpression2 != None:
            res += ": " + str(self.symbolicExpression2)

        return res

    def addElseExpression(self, elseExpression):
        self.symbolicExpression2 = elseExpression

    def getDependencies(self, codeGenerator):
        dep = self.logicalExpression.getDependencies(codeGenerator) + self.symbolicExpression1.getDependencies(codeGenerator)
        
        if self.symbolicExpression2 != None:
            dep += self.symbolicExpression2.getDependencies(codeGenerator)
        
        return list(set(dep))    
        
    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for the identifiers and sets used in this conditional symbolic expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this contitional symbolic expression
        """
        return codeGenerator.generateCode(self)
