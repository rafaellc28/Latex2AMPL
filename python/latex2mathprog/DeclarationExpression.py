from Expression import *

class DeclarationExpression(Expression):
    """
    Class representing a declaration expression node in the AST of a MLP
    """

    def __init__(self, variables, attributeList = None):
        """
        Set the expressions being related
        
        :param variables: VariableList
        :param attributeList: [DeclarationAttribute]
        """
        self.variables = variables
        self.attributeList = attributeList
        
    def __str__(self):
        """
        to string
        """
        res = "DeclarationExpression:" + str(self.variables)
        if self.attributeList != None and len(self.attributeList) > 0:
            res += " " + ",".join(map(lambda el: str(el), self.attributeList))

        return res

    def setAttributeList(self, attributeList):
        self.attributeList = attributeList

    def attrExists(self, attr):
        attrAux = filter(lambda el: el.op == attr.op and str(el.attribute) == str(attr.attribute), self.attributeList)
        if attrAux != None and len(attrAux) > 0:
            return True

        return False

    def addAttribute(self, attribute):
        if self.attributeList == None:
            self.attributeList = []

        if isinstance(attribute, list):
            for attr in attribute:
                if not self.attrExists(attr):
                    self.attributeList.append(attr)
        elif not self.attrExists(attribute):
            self.attributeList.append(attribute)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the variables and sets in this declaration
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this declaration expression
        """
        return codeGenerator.generateCode(self)

class DeclarationAttribute(Expression):
    """
    Class representing a declaration attribute node in the AST of a MLP
    """

    IN  = "in"
    WT  = "within"
    DF  = "default"
    DM  = "dimen"
    ST  = ":="
    EQ  = "="
    LT  = "<"
    LE  = "<="
    GT  = ">"
    GE  = ">="
    NEQ = "!="

    def __init__(self, attribute, op):
        """
        Set the expressions being related
        
        :param attribute: SetExpression | NumericExpression | SymbolicExpression
        """
        self.attribute = attribute
        self.op = op
    
    def __str__(self):
        """
        to string
        """
        return "DeclAttr:" + self.op + " " + str(self.attribute)

    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the variables and sets in this declaration
        """
        codeSetup.setupEnvironment(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this declaration expression
        """
        return codeGenerator.generateCode(self)
