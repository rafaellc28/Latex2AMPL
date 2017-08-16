from Expression import *
from Utils import *

class IndexingExpression(Expression):
    """
    Class representing an indexing expression in the AST of the MLP
    """

    # Get the MathProg code for a given constraint
    @staticmethod
    def _getCodePredicateEntry(entry): return entry.generatePredicateCode()

    def __init__(self, entriesIndexingExpression, logicalExpression = None, stmtIndexing = False):
        """
        Set the entries for the indexing expression
        """

        self.entriesIndexingExpression = entriesIndexingExpression
        self.logicalExpression = logicalExpression
        self.hasSup = False
        self.stmtIndexing = stmtIndexing
        self.supExpression = None

    def __str__(self):
        """
        to string
        """

        res = "\nIE:\n"
        res += "\n".join(filter(Utils._deleteEmpty, map(lambda i: str(i), self.entriesIndexingExpression)))

        if self.logicalExpression:
            res += str(self.logicalExpression)

        return res


    def __len__(self):
        """
        length method
        """

        return len(self.entriesIndexingExpression)

    def add(self, entry):
        """
        Add an entry to the indexing expression
        """

        self.entriesIndexingExpression += [entry]
        return self

    def setLogicalExpression(self, logicalExpression):
        """
        Set the logical expression
        """

        self.logicalExpression = logicalExpression
        return self

    def setStmtIndexing(self, stmtIndexing):
        self.stmtIndexing = stmtIndexing

    def setHasSup(self, hasSup):
        self.hasSup = hasSup

    def setSupExpression(self, supExpression):
        self.supExpression = supExpression

    def getDependencies(self, codeGenerator):
        dep = Utils._flatten(map(lambda el: el.getDependencies(codeGenerator), self.entriesIndexingExpression))
        
        if self.logicalExpression != None:
            dep += self.logicalExpression.getDependencies(codeGenerator)
        
        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this indexing expression
        """
        return codeGenerator.generateCode(self)
