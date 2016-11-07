from Expression import *

class EntryLogicalExpression(Expression):
    """
    Class representing an entry of logical expression in the AST of the MLP
    """

class EntryLogicalExpressionRelational(EntryLogicalExpression):
    """
    Class representing an entry of relational logical expression in the AST of the MLP
    """

    LT = "<"
    LE = "<="
    EQ = "="
    GE = ">="
    NEQ = "<>"

    def __init__(self, op, numericExpression1, numericExpression2):
        """
        Set the operator and the numeric expressions

        :param op : (LT, LE, EQ, GE, NEQ)
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """

        self.op = op
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2

    def __str__(self):
        """
        to string
        """

        return str(self.numericExpression1) + " " + self.op + " " + str(self.numericExpression2)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry of Relational Logical Expression
        """
        return codeGenerator.generateCode(self)
    

class EntryLogicalExpressionWithSet(EntryLogicalExpression):
    """
    Class representing an entry of logical expression with sets in the AST of the MLP
    """

    IN = "in"
    NOTIN = "not in"

    def __init__(self, op, value, setExpression):
        """
        Set the operator, the value and the set expression

        :param op : op
        :param value : ValueList| Variable | TupleList
        :param setExpression : setExpression
        """

        self.op = op
        self.value = value
        self.setExpression = setExpression
        self.isBinary = False
        self.isInteger = False
        self.isNatural = False
        self.isReal = False

    def __str__(self):
        """
        to string
        """

        return str(self.value) + " " + self.op + " " + str(self.setExpression)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry of Logical Expression with Set
        """
        return codeGenerator.generateCode(self)


class EntryLogicalExpressionWithSetOperation(EntryLogicalExpression):
    """
    Class representing an entry of logical expression with sets in the AST of the MLP
    """

    SUBSET = "within"
    NOTSUBSET = "not within"

    def __init__(self, op, setExpression1, setExpression2):
        """
        Set the operator and the set expressions

        :param op : (SUBSET, NOTSUBSET)
        :param setExpression1 : SetExpression
        :param setExpression2 : SetExpression
        """

        self.op = op
        self.setExpression1 = setExpression1
        self.setExpression2 = setExpression2

    def __str__(self):
        """
        to string
        """

        return str(self.setExpression1) + " " + self.op + " " + str(self.setExpression2)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry of Logical Expression with Set
        """
        return codeGenerator.generateCode(self)


class EntryLogicalExpressionIterated(EntryLogicalExpression):
    """
    Class representing an entry of iterated logical expression in the AST of the MLP
    """

    FORALL = "forall"
    EXISTS = "exists"

    def __init__(self, op, indexingExpression, logicalExpression):
        """
        Set the operator and the numeric expressions

        :param op : (FORALL, EXISTS)
        :param indexingExpression : IndexingExpression
        :param logicalExpression  : LogicalExpression
        """

        self.op = op
        self.indexingExpression = indexingExpression
        self.logicalExpression  = logicalExpression

    def __str__(self):
        """
        to string
        """

        return self.op + "{" + str(self.indexingExpression) + "} " +  str(self.logicalExpression)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for Entry of Iterated Logical Expression
        """
        return codeGenerator.generateCode(self)
        

class EntryLogicalExpressionBetweenParenthesis(EntryLogicalExpression):
    """
    Class representing a logical expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, logicalExpression):
        """
        Set the logical expression

        :param logicalExpression : LogicalExpression
        """

        self.logicalExpression = logicalExpression

    def __str__(self):
        """
        to string
        """
        
        return "LE: (" + str(self.logicalExpression) + ")"
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the variables and sets used in this logical expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this logical expression
        """
        return codeGenerator.generateCode(self)
