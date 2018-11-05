from Expression import *

class NodeExpression(Expression):
    """
    Class representing a node expression node in the AST of a MLP
    """

    
    NETOUT = "net_out"

    LE = "<="
    GE = ">="
    EQ = "="

    def __init__(self, identifier, netExpression, op, value, indexingExpression = None):
        """
        Set the constraint expression and the indexing expression of a node expression
        
        :param identifier: Identifier
        :param netExpression: NumericExpression
        :param op: LE | GE | EQ
        :param value: Identifier | NumericSymbolicExpression
        :param indexingExpressions: IndexingExpression
        """
        
        self.identifier = identifier
        self.netExpression = netExpression
        self.op = op
        self.value = value
        self.indexingExpression   = indexingExpression
    
    def __str__(self):
        """
        to string
        """
        
        res = str(self.identifier) + " " + str(self.netExpression) + " " + str(self.op) + " " + str(self.value)

        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return "Node Expression: " + res

    def getDependencies(self, codeGenerator):
        deps = self.identifier.getDependencies(codeGenerator) + self.value.getDependencies(codeGenerator)

        if self.indexingExpression:
            deps += self.indexingExpression.getDependencies(codeGenerator)

        return list(set(deps))

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for declaration of identifiers and sets in this node expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this node expression
        """
        return codeGenerator.generateCode(self)

class NetInExpression(Expression):
    """
    Class representing a net_in expression node in the AST of a MLP
    """
    NETIN = "net_in"

    def __init__(self):
        """
        Set the constraint expression and the indexing expression of a node expression
        """
    
    def __str__(self):
        """
        to string
        """
        
        return NetInExpression.NETIN

    def getDependencies(self, codeGenerator):
        return []

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for declaration of identifiers and sets in this net_in expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this net_in expression
        """
        return codeGenerator.generateCode(self)

class NetOutExpression(Expression):
    """
    Class representing a net_in expression node in the AST of a MLP
    """
    NETOUT = "net_out"

    def __init__(self):
        """
        Set the constraint expression and the indexing expression of a node expression
        """
    
    def __str__(self):
        """
        to string
        """
        
        return NetOutExpression.NETOUT

    def getDependencies(self, codeGenerator):
        return []

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for declaration of identifiers and sets in this net_in expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this net_in expression
        """
        return codeGenerator.generateCode(self)
