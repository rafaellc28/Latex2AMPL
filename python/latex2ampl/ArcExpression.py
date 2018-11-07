from Expression import *

class ArcExpression(Expression):
    """
    Class representing an arc expression node in the AST of a MLP
    """

    def __init__(self, identifier, attributes, _from, to, objName, objValue, indexingExpression = None):
        """
        Set the constraint expression and the indexing expression of an arc expression
        
        >param identifier: Identifier
        :param attributes: [DeclarationAttribute]
        :param _from: Identifier
        :param to: Identifier
        :param objName: Identifier
        :param objValue: Identifier
        :param indexingExpressions: IndexingExpression
        """
        
        self.identifier = identifier
        self.attributes = attributes
        self._from   = _from
        self.to   = to
        self.objName   = objName
        self.objValue   = objValue
        self.indexingExpression   = indexingExpression
        
    def __str__(self):
        """
        to string
        """
        res = "Arc Expression: " + str(self.identifier) + " "

        if self.attributes and len(self.attributes) > 0:
            res += ", ".join(map(lambda el: str(el), self.attributes))

        if self._from:
            res += " from " + str(self._from)

        if self.to:
            res += " to " + str(self.to)

        if self.objName:
            res += " obj " + str(self.objName) + " " + str(self.objValue)

        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return res

    def getDependencies(self, codeGenerator):
        deps = self.identifier.getDependencies(codeGenerator)

        if self.attributes and len(self.attributes) > 0:
            deps += map(lambda el: el.getDependencies(codeGenerator), self.attributes)

        if self._from:
            deps += self._from.getDependencies(codeGenerator)

        if self.to:
            deps += self.to.getDependencies(codeGenerator)

        if self.objName:
            deps += self.objName.getDependencies(codeGenerator) + self.objValue.getDependencies(codeGenerator)

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
