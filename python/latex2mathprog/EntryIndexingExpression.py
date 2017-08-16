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
    
    def __init__(self, identifier, setExpression, op = IN):
        """
        Set the identifier(s) and the set

        :param identifier    : Identifier | ValueList
        :param setExpression : SetExpression
        :param op            : (IN | NOTIN)
        """

        self.identifier    = identifier
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

        if isinstance(self.identifier, ValueList):
            return "EIE_S: ValueList: [" + ", ".join(map(lambda var: str(var) + " " + self.op + " " + str(self.setExpression), self.identifier)) + "]"
        else:
            return "EIE_S: " + str(self.identifier) + " " + self.op + " " + str(self.setExpression)
    
    def getDependencies(self, codeGenerator):
        return list(set(self.identifier.getDependencies(codeGenerator) + self.setExpression.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of identifiers and sets used in this entry for indexing expression
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

    def __init__(self, op, identifier, numericExpression):
        """
        Set the identifier and the numeric expression being compared, and the comparison operator

        :param op                : op
        :param identifier        : Identifier
        :param numericExpression : NumericExpression
        """

        self.op                = op
        self.identifier        = identifier
        self.numericExpression = numericExpression

    def __str__(self):
        """
        to string
        """

        return "EIE_C: " + str(self.identifier) + " " + self.op + " " + str(self.numericExpression)

    def getDependencies(self, codeGenerator):
        return list(set(self.identifier.getDependencies(codeGenerator) + self.numericExpression.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of identifiers and sets used in this entry for indexing expressions
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
    
    def __init__(self, op, identifier, value, supExpression = None):
        """
        Set the identifier and the value it receives
        
        :param               : op
        :param identifier    : Identifier
        :param value         : Value | Range
        :param supExpression : Expression
        """

        self.op         = op
        self.identifier = identifier
        self.value      = value
        self.supExpression = supExpression
        self.hasSup = False
        

    def __str__(self):
        """
        to string
        """

        return "EIE_E: " + str(self.identifier) + " " + self.op + " " + str(self.value)
    
    def setHasSup(self, value):
        """
        Set if the entry expression has a sup value
        """
        self.hasSup = value

    def setSupExpression(self, supExpression):
        self.supExpression = supExpression
    
    def getDependencies(self, codeGenerator):
        dep = self.identifier.getDependencies(codeGenerator) + self.value.getDependencies(codeGenerator)

        if self.supExpression != None:
            dep += self.supExpression.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of identifiers and sets used in this entry for indexing expressions
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry with Equality of Indexing Expression
        """
        return codeGenerator.generateCode(self)
