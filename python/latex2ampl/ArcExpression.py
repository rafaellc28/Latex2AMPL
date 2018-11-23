from Expression import *

class ArcExpression(Expression):
    """
    Class representing an arc expression node in the AST of a MLP
    """

    def __init__(self, identifier, attributes, _from, to, _obj, indexingExpression = None):
        """
        Set the attributes of an arc expression
        
        :param identifier: Identifier
        :param attributes: [DeclarationAttribute]
        :param _from: [ArcItem]
        :param to: [ArcItem]
        :param _obj: ArcObj
        :param indexingExpressions: IndexingExpression
        """
        
        self.identifier = identifier
        self.attributes = attributes
        self._from = _from
        self.to = to
        self._obj = _obj
        self.indexingExpression   = indexingExpression
        
    def __str__(self):
        """
        to string
        """
        res = "ArcExpression: " + str(self.identifier) + " "

        if self.attributes and len(self.attributes) > 0:
            res += ", ".join(map(lambda el: str(el), self.attributes))

        if self._from and len(self._from) > 0:
            res += " from " + ", ".join(map(lambda el: str(el), self._from))

        if self.to and len(self.to) > 0:
            res += " to " + ", ".join(map(lambda el: str(el), self.to))

        if self._obj:
            res += " " + str(self._obj)

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

        if self._obj:
            deps += self._obj.getDependencies(codeGenerator)

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


class ArcItem(Expression):
    """
    Class representing an arc item expression node in the AST of a MLP
    """

    def __init__(self, identifier, factor = None, indexingExpression = None):
        """
        Set the attributes of an arc item expression
        
        :param identifier: Identifier
        :param factor: NumericSymboLicExpression
        :param indexingExpression: LogicalIndexExpression | IndexingExpression
        """
        
        self.identifier = identifier
        self.factor = factor
        self.indexingExpression = indexingExpression
        
    def __str__(self):
        """
        to string
        """
        res = "ArcItem: " + str(self.identifier) + " "

        if self.indexingExpression:
            res += "{"+str(self.indexingExpression)+"}"

        if self.factor:
            res += str(self.factor)

        return res

    def getDependencies(self, codeGenerator):
        deps = self.identifier.getDependencies(codeGenerator)

        if self.indexingExpression:
            deps += self.indexingExpression.getDependencies(codeGenerator)

        if self.factor:
            deps += self.factor.getDependencies(codeGenerator)

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

class ArcObj(Expression):
    """
    Class representing an arc item expression node in the AST of a MLP
    """

    def __init__(self, name, value, indexingExpression = None):
        """
        Set the attributes of an arc item expression
        
        :param name: Identifier
        :param value: NumericSymboLicExpression | Identifier
        :param indexingExpression: IndexingExpression
        """
        
        self.name = name
        self.value = value
        self.indexingExpression = indexingExpression
        
    def __str__(self):
        """
        to string
        """
        res = "ArcObj: " + str(self.name)

        if self.indexingExpression:
            res += " {"+str(self.indexingExpression)+"}"

        if self.value:
            res += " " + str(self.value)

        return res

    def getDependencies(self, codeGenerator):
        deps = self.name.getDependencies(codeGenerator)

        if self.indexingExpression:
            deps += self.indexingExpression.getDependencies(codeGenerator)

        if self.value:
            deps += self.value.getDependencies(codeGenerator)

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
