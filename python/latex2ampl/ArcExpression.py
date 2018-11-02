from Expression import *

class ArcExpression(Expression):
    """
    Class representing an arc expression node in the AST of a MLP
    """

    def __init__(self, identifier, lowerLimit, upperLimit, _from, to, objName, objValue, indexingExpression = None):
        """
        Set the constraint expression and the indexing expression of an arc expression
        
        >param identifier: Identifier
        :param lowerLimit: NumericSymbolicExpression
        :param upperLimit: NumericSymbolicExpression
        :param _from: Identifier
        :param to: Identifier
        :param objName: Identifier
        :param objValue: Identifier
        :param indexingExpressions: IndexingExpression
        """
        
        self.identifier = identifier
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self._from   = _from
        self.to   = to
        self.objName   = objName
        self.objValue   = objValue
        self.indexingExpression   = indexingExpression
        
    def __str__(self):
        """
        to string
        """
        res = "Arc Expression: " + str(self.identifier) + " >= " + str(self.lowerLimit) + ", <= " + str(self.upperLimit) + " from " + \
                str(self._from) + " to " + str(self.to) + " obj " + str(self.objName) + " " + str(self.objValue)

        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return res

    def getDependencies(self, codeGenerator):
        deps = self.identifier.getDependencies(codeGenerator) + self.lowerLimit.getDependencies(codeGenerator) + self.upperLimit.getDependencies(codeGenerator) +\
            self._from.getDependencies(codeGenerator) + self.to.getDependencies(codeGenerator) + self.objName.getDependencies(codeGenerator) + \
            self.objValue.getDependencies(codeGenerator)

        if self.indexingExpression:
            deps += self.indexingExpression.getDependencies(codeGenerator)

        return list(set(deps))

    def setupEnvironment(self, codeSetup):
        """
        Generate the AMPL code for declaration of identifiers and sets in this arc expression
        """
        codeSetup.setupEnvironment(self)
        
    def generateCode(self, codeGenerator):
        """
        Generate the AMPL code for this arc expression
        """
        return codeGenerator.generateCode(self)
