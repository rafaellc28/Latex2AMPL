from Expression import *

class NodeExpression(Expression):
    """
    Class representing a node expression node in the AST of a MLP
    """

    
    LE = "<="
    GE = ">="
    EQ = "="

    def __init__(self, identifier, op = None, expression1 = None, expression2 = None, expression3 = None, indexingExpression = None):
        """
        Set the constraint expression and the indexing expression of a node expression
        
        :param identifier: Identifier
        :param op: LE | GE | EQ
        :param expression1: Identifier | NumericSymbolicExpression
        :param expression2: Identifier | NumericSymbolicExpression
        :param expression3: Identifier | NumericSymbolicExpression
        :param indexingExpressions: IndexingExpression
        """
        
        self.identifier = identifier
        self.op = op
        self.expression1 = expression1
        self.expression2 = expression2
        self.expression3 = expression3
        self.indexingExpression   = indexingExpression
    
    def __str__(self):
        """
        to string
        """
        
        res = str(self.identifier)

        if self.expression1:
            res += " " + str(self.expression1)

        if self.op:
            res += " " + str(self.op)

        if self.expression2:
            res += " " + str(self.expression2)

        if self.expression3:
            if self.op:
                res += " " + str(self.op)

            res += " " + str(self.expression3)

        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return "Node Expression: " + res

    def getDependencies(self, codeGenerator):
        deps = self.identifier.getDependencies(codeGenerator)
        
        if self.expression1:
            deps += self.expression1.getDependencies(codeGenerator)

        if self.expression1:
            deps += self.expression2.getDependencies(codeGenerator)

        if self.expression3:
            deps += self.expression3.getDependencies(codeGenerator)

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
