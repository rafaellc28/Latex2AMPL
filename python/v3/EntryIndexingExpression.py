from Expression import *
from ValueList import *

class EntryIndexingExpression(Expression):
    """
    Class representing an entry of indexing expression in the AST of the MLP
    """

class EntryIndexingExpressionWithSet(EntryIndexingExpression):
    """
    Class representing an entry with set of indexing expression in the AST of the MLP
    """

    IN = "in"
    NOTIN = "not in"

    def __init__(self, variable, setExpression, op = IN):
        """
        Set the variable(s) and the set

        :param variable      : Variable | ValueList
        :param setExpression : SetExpression
        :param op            : (IN | NOTIN)
        """

        self.variable      = variable
        self.setExpression = setExpression
        self.op = op
        self.isBinary = False
        self.isInteger = False
        self.isNatural = False
        self.isReal = False
        self.isSymbolic = False
        self.isLogical = False
        self.isDeclaredAsVar = False
        self.isDeclaredAsSet = False
        self.isDeclaredAsParam = False

    def __str__(self):
        """
        to string
        """

        if isinstance(self.variable, ValueList):
            return "EIE_S: ValueList: [" + ", ".join(map(lambda var: str(var) + " " + self.op + " " + str(self.setExpression), self.variable)) + "]"
        else:
            return "EIE_S: " + str(self.variable) + " " + self.op + " " + str(self.setExpression)
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for indexing expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry with Set of Indexing Expression
        """
        return codeGenerator.generateCode(self)

# This type of comparison is used only as a predicate of an entry in an indexing expression
class EntryIndexingExpressionCmp(EntryIndexingExpression):
    """
    Class representing an entry with comparison operator of indexing expression in the AST of the MLP
    """

    NEQ = "<>"
    LE  = "<="
    GE  = ">="
    LT  = "<"
    GT  = ">"

    def __init__(self, op, variable, numericExpression):
        """
        Set the variable and the numeric expression being compared, and the comparison operator

        :param op                : op
        :param variable          : Variable
        :param numericExpression : NumericExpression
        """

        self.op                = op
        self.variable          = variable
        self.numericExpression = numericExpression
        self.internalSet       = 0

    def __str__(self):
        """
        to string
        """

        return "EIE_C: " + str(self.variable) + " " + self.op + " " + str(self.numericExpression)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of variables and sets used in this entry for indexing expressions
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry with Comparison of Indexing Expression
        """
        return codeGenerator.generateCode(self)
        

class EntryIndexingExpressionEq(EntryIndexingExpression):
    """
    Class representing an entry with equality operator of indexing expression in the AST of the MLP
    """

    EQ = "="
    NEQ = "!=" # delete this constant, make no sense a indexing expression with inequality instead of equality
    
    def __init__(self, op, variable, value, supExpression = None):
        """
        Set the variable and the numeric expression being compared, and the comparison operator

        :param          : op
        :param variable : Variable
        :param value    : Value | Range
        """

        self.op       = op
        self.variable = variable
        self.value    = value
        self.internalSet = 0
        self.hasSup = False
        self.supExpression = supExpression

    def __str__(self):
        """
        to string
        """

        return "EIE_E: " + str(self.variable) + " " + self.op + " " + str(self.value)
    
    def setHasSup(self, value):
        """
        Set if the entry expression has a sup value
        """
        self.hasSup = value

    def setSupExpression(self, supExpression):
        self.supExpression = supExpression
    
    def setInternalSet(internalSet):
        self.internalSet = internalSet
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of variables and sets used in this entry for indexing expressions
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry with Equality of Indexing Expression
        """
        return codeGenerator.generateCode(self)
