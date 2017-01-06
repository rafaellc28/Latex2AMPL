from Expression import *

class ValueList(Expression):
    """
    Class representing a list of values in the AST of the MLP
    """

    def __init__(self, values):
        """
        Set the values
        
        :param values : [Variable|Number]
        :param setExpression : SetExpression
        """
        
        self.values = values
        self.i = -1

    def __str__(self):
        """
        to string
        """
        
        return "ValueList: [" + ",".join(map(lambda i: str(i), self.values)) + "]"

    def __len__(self):
        """
        length method
        """

        return len(self.values)

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.values)-1:
            self.i += 1         
            return self.values[self.i]
        else:
            self.i = -1
            raise StopIteration
    
    def getValues(self):
        """
        get the values in this ValueList
        """

        return self.values

    def add(self, value):
        """
        Add a value to the list
        """

        self.values += [value]
        return self

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Range
        """
        return codeGenerator.generateCode(self)
