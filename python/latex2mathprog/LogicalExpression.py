from Expression import *
from Utils import *

class LogicalExpression(Expression):
    """
    Class representing an logical expression in the AST of the MLP
    """

    def __init__(self, entriesLogicalExpression):
        """
        Set the entries for the logical expression
        """

        self.entriesLogicalExpression = map(lambda e: {"and": e}, entriesLogicalExpression)

    def __str__(self):
        """
        to string
        """
        res = "\nLE:\n"
        resAux = ""
        first = True

        for i in range(len(self.entriesLogicalExpression)):
            for conj in self.entriesLogicalExpression[i]:
                code = str(self.entriesLogicalExpression[i][conj])

                if code != 0:
                    if first:
                        first = False
                        res += code
                    else:
                        res += " " + conj + " " + code

        return res + resAux

    def __len__(self):
        """
        length method
        """

        return len(self.entriesLogicalExpression)

    def addAnd(self, entry):
        """
        Add an entry to the logical expression with and conjunctor
        """

        self.entriesLogicalExpression.append({"and": entry})
        return self

    def addOr(self, entry):
        """
        Add an entry to the logical expression with or conjunctor
        """

        self.entriesLogicalExpression.append({"or": entry})
        return self
    
    def getDependencies(self, codeGenerator):
        entries = [v for e in self.entriesLogicalExpression for k,v in e.iteritems()]
        return list(set(Utils._flatten(map(lambda el: el.getDependencies(codeGenerator), entries))))


    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this logical expression
        """
        return codeGenerator.generateCode(self)
