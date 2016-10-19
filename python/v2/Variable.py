from Expression import *
from ID import *
from Number import *

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
        self.inSets = []
        self.isSet = False
        self.isParam = False

    def __str__(self):
        """
        to string
        """
        
        if len(self.sub_indices) > 0:
            if isinstance(self.sub_indices, Variable) or isinstance(self.sub_indices, ID) or isinstance(self.sub_indices, Number):
                res = str(self.variable) + "[" + str(self.sub_indices) + "]"
            else:
                res = str(self.variable) + "[" + ",".join(map(lambda i: str(i), self.sub_indices)) + "]"
        else:
            res = str(self.variable)
        
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

    def setIsSet(self, isSet):
        self.isSet = isSet

    def setIsParam(self, isParam):
        self.isParam = isParam

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
