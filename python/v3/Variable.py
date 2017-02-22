from Expression import *
from ID import *
from Number import *
from NumericExpression import *

class Variable(Expression):
    """
    Class representing an Variable in the AST of the MLP
    """
    
    def __init__(self, variable, sub_indices = []):
        """
        Set the variable and the sub indices (if there are)
        
        :param variable: ID
        :param sub_indices: [ID|Number]
        """
        Expression.__init__(self)
        
        self.variable = variable
        self.sub_indices = sub_indices
        self.dimenSet = 1
        self.isInSet = False
        self.isSet = None
        self.isVar = None
        self.isParam = None
        self.isReal = False
        self.isSymbolic = False
        self.isLogical = False
        self.isSubIndice = False
        self.isDeclaredAsParam = None
        self.isDeclaredAsSet = None
        self.isDeclaredAsVar = None

    def __str__(self):
        """
        to string
        """
        
        var = ""
        if self.isSet and isinstance(self.dimenSet, int) and self.dimenSet > 1:
            var += str(self.variable) + "{"+str(self.dimenSet)+"}"
        else:
            var += str(self.variable)

        if len(self.sub_indices) > 0:
            if isinstance(self.sub_indices, Variable) or isinstance(self.sub_indices, ID) or isinstance(self.sub_indices, Number) or isinstance(self.sub_indices, NumericExpression):
                res = var + "[" + str(self.sub_indices) + "]"
            else:
                res = var + "[" + ",".join(map(lambda i: str(i), self.sub_indices)) + "]"
        else:
            res = var
        
        return "Var:" + res

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
    
    def addSet(self, inSet):
        self.inSets += [inSet]

    def setIsInSet(self, isInSet):
        self.isInSet = isInSet
    
    def setIsSet(self, isSet):
        self.isSet = isSet

    def setIsParam(self, isParam):
        self.isParam = isParam

    def setIsSymbolic(self, isSymbolic):
        self.isSymbolic = isSymbolic

    def setIsLogical(self, isLogical):
        self.isLogical = isLogical

    def setDimenSet(self, dimen):
        self.dimenSet = dimen

    def setIsVar(self, isVar):
        self.isVar = isVar

    def setIsSubIndice(self, isSubIndice):
        self.isSubIndice = isSubIndice

    def setSubIndices(self, subIndices):
        self.sub_indices = subIndices
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of this variable
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Variable
        """
        return codeGenerator.generateCode(self)
    
    def generateCodeWithoutIndices(self, codeGenerator):
        """
        Generate the MathProg code for this Variable without the Indexing, if there are 
        """
        return self.variable.generateCode(codeGenerator)
