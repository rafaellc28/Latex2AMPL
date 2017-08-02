class Declarations:
    """
    Class that encapsulate a list of all nodes in the AST that represent a declaration in a MLP
    """

    def __init__(self, declarations):
        """
        Set the list of declarations
        
        :param declarations: [Declaration]
        """
        
        self.declarations = declarations
    
    def __str__(self):
        """
        to string
        """
        
        return "\nDecls:\n" + "\n".join(map(lambda i: str(i), self.declarations))
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the identifiers and sets used in these declarations
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the code in MathProg for these Constraints
        """
        return codeGenerator.generateCode(self)
    
class Declaration:
    """
    Class representing a declaration node in the AST of a MLP
    """
    
    # Get the MathProg code for a given IndexingExpression
    @staticmethod
    def _getCodeIndexingExpression(indexingExpression): return indexingExpression.generateCode()
    #def _getCodeIndexingExpression(indexingExpression): return SupportGenCode.emitIndexingExpression(indexingExpression.generateCode())

    def __init__(self, declarationExpression, indexingExpression = None, stmtIndex = False):
        """
        Set the declaration expression and the indexing expression of an declaration
        
        :param declarationExpression: DeclarationExpression
        :param indexingExpressions: IndexingExpression
        """
        
        self.declarationExpression = declarationExpression
        self.indexingExpression   = indexingExpression
        self.stmtIndex = stmtIndex
    
    def __str__(self):
        """
        to string
        """
        res = str(self.declarationExpression)
        
        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return "Decl:" + res
    
    def setStmtIndexing(self, stmtIndex):
        self.stmtIndex = stmtIndex

    def setIndexingExpression(self, indexingExpression):
        self.indexingExpression = indexingExpression
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for declaration of identifiers and sets in this declaration
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this constraint
        """
        return codeGenerator.generateCode(self)
