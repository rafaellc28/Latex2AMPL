from Expression import *

class TupleList(Expression):
    """
    Class representing a list of values in the AST of the MLP
    """

    def __init__(self, values):
        """
        Set the values
        
        :param values : [Identifier|Number]
        """
        
        self.values = values
        self.i = -1

    def __str__(self):
        """
        to string
        """
        
        return "TupleList: [" + ",".join(map(lambda i: str(i), self.values)) + "]"

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
        Get the values in this TupleList
        """

        return self.values

    def add(self, value):
        """
        Add a value to the list
        """

        self.values += [value]
        return self
    
    def getDependencies(self):
        return list(set(Utils._flatten(map(lambda el: el.getDependencies(), self.values))))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of identifiers used in this tuple list expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this TupleList
        """
        return codeGenerator.generateCode(self)
