from Utils import *
from TupleList import *
from ValueList import *
from Variable import *

class CodeSetup:
    """ Visitor in the Visitor Pattern """

    def __init__(self, codeGenerator = None):
        self.codeGenerator = codeGenerator
        self.varKey = None
        self.Stm = None

    def setupEnvironment(self, node):
        cls = node.__class__
        method_name = 'setupEnvironment_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    # Auxiliary Methods

    def _addDomainAux(self, variable, domain):
        self.codeGenerator.Types[variable.generateCodeWithoutIndices(self.codeGenerator)] = domain

    def _addDomain(self, variable, domain):
        if isinstance(variable, ValueList):
            for var in variable.getValues():
                self._addDomainAux(var, domain)
        else:
            self._addDomainAux(variable, domain)

    def _addIndiceAux(self, variable, setExpression):
        ind = variable.generateCode(self.codeGenerator)
        if ind in self.codeGenerator.Indices:
            self.codeGenerator.Indices[ind] = setExpression

    def _addIndice(self, variable, setExpression):
            if isinstance(variable, ValueList):
                for var in variable.getValues():
                    self._addIndiceAux(var, setExpression)
            else:
                self._addIndiceAux(variable, setExpression)

    # Get the MathProg code for a given sub-indice
    def _getCodeID(self, id_):
        val = id_.generateCode(self.codeGenerator)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given constraint
    def _setupConstraint(self, constraint):
        constraint.setupEnvironment(self)

    # Get the MathProg code for a given constraint
    def _setupEntry(self, entry): return entry.setupEnvironment(self)

    # Get the MathProg code for a given entry
    def _setupEntryByKey(self, entry):
        for key in entry:
            return entry[key].setupEnvironment(self)

    def _setupValue(self, value):
        value.setupEnvironment(self)

    def _checkSubIndices(self, node):
        if Utils._isInstanceOfStr(node.sub_indices):
            return 

        if len(node.sub_indices) > 0:
            if Utils._isInstanceOfList(node.sub_indices):
                for i in range(len(node.sub_indices)):
                    node.sub_indices[i].setIndice(i)
                    node.sub_indices[i].setupEnvironment(self)

            else:
                node.sub_indices.setIndice(0)
                node.sub_indices.setupEnvironment(self)

    def _setupEnvironment_SubIndice(self, node):
        ind = node.generateCode(self.codeGenerator)
        self.Stm[self.varKey]["sub-indices"][node.getIndice()]["var"] = ind
        
        if not ind in self.codeGenerator.Indices:
            self.codeGenerator.Indices[ind] = ""

    # Linear Program
    def setupEnvironment_LinearProgram(self, node):
        """
        Generate the MathProg code for the Set, Parameter and Variable statements
        """

        node.objective.setupEnvironment(self)
        if node.constraints:
            node.constraints.setupEnvironment(self)

    # Objective
    def setupEnvironment_Objective(self, node):
        """
        Generate the MathProg code for the variables and sets used in this objective function
        """
        node.linearExpression.setupEnvironment(self)

        if node.domain:
            node.domain.setupEnvironment(self)

    # Constraints
    def setupEnvironment_Constraints(self, node):
        """
        Generate the MathProg code for the variables and sets used in these constraints
        """
        map(self._setupConstraint, node.constraints)

    # Constraint
    def setupEnvironment_Constraint(self, node):
        """
        Generate the MathProg code for declaration of variables and sets in this constraint
        """
        node.constraintExpression.setupEnvironment(self)

        if node.indexingExpression:
            node.indexingExpression.setupEnvironment(self)

    def setupEnvironment_ConstraintExpression2(self, node):
        """
        Generate the MathProg code for the variables and sets in this constraint
        """
        node.linearExpression1.setupEnvironment(self)
        node.linearExpression2.setupEnvironment(self)

    def setupEnvironment_ConstraintExpression3(self, node):
        """
        Generate the MathProg code for the variables and sets in this constraint
        """
        node.linearExpression.setupEnvironment(self)
        node.numericExpression1.setupEnvironment(self)
        node.numericExpression2.setupEnvironment(self)

    # Linear Expression
    def setupEnvironment_ValuedLinearExpression(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """
        node.value.setupEnvironment(self)

    def setupEnvironment_LinearExpressionBetweenParenthesis(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """
        node.linearExpression.setupEnvironment(self)

    def setupEnvironment_LinearExpressionWithArithmeticOperation(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """
        node.expression1.setupEnvironment(self)
        node.expression2.setupEnvironment(self)

    def setupEnvironment_MinusLinearExpression(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """
        node.linearExpression.setupEnvironment(self)

    def setupEnvironment_IteratedLinearExpression(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets in this linear expression
        """
        if node.numericExpression:
            node.numericExpression.setupEnvironment(self)
            node.indexingExpression.setHasSup(True)
        
        node.linearExpression.setupEnvironment(self)
        node.indexingExpression.setupEnvironment(self)

    # Numeric Expression
    def setupEnvironment_NumericExpressionWithFunction(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_ValuedNumericExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        node.value.setupEnvironment(self)

    def setupEnvironment_NumericExpressionBetweenParenthesis(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_NumericExpressionWithArithmeticOperation(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        node.numericExpression1.setupEnvironment(self)
        node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_MinusNumericExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_IteratedNumericExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.supNumericExpression:
            node.supNumericExpression.setupEnvironment(self)
            node.indexingExpression.setHasSup(True)
        
        node.numericExpression.setupEnvironment(self)
        node.indexingExpression.setupEnvironment(self)

    # Indexing Expression
    def setupEnvironment_IndexingExpression(self, node):
        """
        Generate the MathProg code for entries in this indexing expression
        """
        if node.hasSup:
            if len(node.entriesIndexingExpression) != 1:
                raise Exception('If iterated expression has a superior expression, then it must have a single entry!')
            #elif Utils._isInstanceOfStr(node.entriesIndexingExpression[0]) or not node.entriesIndexingExpression[0].isInstanceOfEntryIndexingExpressionEq():
            #    raise Exception('If iterated expression has a superior expression, then its single entry must be of type EntryIndexingExpressionEq!')
            else:
                node.entriesIndexingExpression[0].setHasSup(True)

        map(self._setupEntry, node.entriesIndexingExpression)

        if node.logicalExpression:
            node.logicalExpression.setupEnvironment(self)

    def setupEnvironment_EntryExpressionWithSet(self, node, variable):
        if isinstance(variable, Variable) and len(variable.sub_indices) > 0:
            variable.setupEnvironment(self)
        elif isinstance(variable, ValueList):
            for var in variable.getValues():
                if len(var.sub_indices) > 0:
                    var.setupEnvironment(self)

        setCode = node.setExpression.generateCode(self.codeGenerator)
        setCode = setCode.replace(" ", "")

        if setCode == "0,1":
            node.isBinary = True
            self._addDomain(variable, "binary")

        elif setCode == "integer":
            node.isInteger = True
            self._addDomain(variable, "integer")

        elif setCode == "natural":
            node.isNatural = True
            self._addDomain(variable, "integer, >= 0")

        elif setCode == "real":
            node.isReal = True
            self._addDomain(variable, "")

        self._addIndice(variable, setCode)

    # Entry Indexing Expression
    def setupEnvironment_EntryIndexingExpressionWithSet(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for indexing expression
        """

        if Utils._isInstanceOfStr(node.variable):
            return

        if isinstance(node.variable, TupleList):
            self.codeGenerator.Tuples[node.setExpression.generateCode(self.codeGenerator)] = {}
            self.codeGenerator.Tuples[node.setExpression.generateCode(self.codeGenerator)]["tuple"] = map(lambda val: val.generateCode(self.codeGenerator), node.variable.getValues())
            self.codeGenerator.Tuples[node.setExpression.generateCode(self.codeGenerator)]["op"] = node.op

        else:
            self.setupEnvironment_EntryExpressionWithSet(node, node.variable)

        node.setExpression.setupEnvironment(self)

    def setupEnvironment_EntryIndexingExpressionCmp(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this entry for indexing expressions
        """
        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_EntryIndexingExpressionEq(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this entry for indexing expressions
        """
        ind = node.variable.generateCode(self.codeGenerator)
        if ind in self.codeGenerator.Indices:
            self.codeGenerator.Indices[ind] = node.value.generateCode(self.codeGenerator)

        node.value.setupEnvironment(self)

    def setupEnvironment_LogicalExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        map(self._setupEntryByKey, node.entriesLogicalExpression)

    # Entry Logical Expression
    def setupEnvironment_EntryLogicalExpressionRelational(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        node.numericExpression1.setupEnvironment(self)
        node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionWithSet(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """

        if Utils._isInstanceOfStr(node.value):
            return

        self.setupEnvironment_EntryExpressionWithSet(node, node.value)
        
        node.setExpression.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionWithSetOperation(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        node.setExpression1.setupEnvironment(self)
        node.setExpression2.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionIterated(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        node.indexingExpression.setupEnvironment(self)
        node.logicalExpression.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionBetweenParenthesis(self, node):
        """
        Generate the MathProg code for the variables and sets used in this logical expression
        """
        node.logicalExpression.setupEnvironment(self)

    # Set Expression
    def setupEnvironment_SetExpressionWithValue(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        if not Utils._isInstanceOfStr(node.value):
            if isinstance(node.value, Variable):
                node.value.setIsSet(True)

            node.value.setupEnvironment(self)

    def setupEnvironment_SetExpressionWithIndices(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        if not Utils._isInstanceOfStr(node.variable):
            node.variable.setIsSet(True)
            node.variable.setupEnvironment(self)

    def setupEnvironment_SetExpressionWithOperation(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        node.setExpression1.setupEnvironment(self)
        node.setExpression2.setupEnvironment(self)

    # Range
    def setupEnvironment_Range(self, node):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        if not Utils._isInstanceOfStr(node.rangeInit):
            if isinstance(node.rangeInit, Variable):
                node.rangeInit.setIsParam(True)

        if not Utils._isInstanceOfStr(node.rangeEnd):
            if isinstance(node.rangeEnd, Variable):
                node.rangeEnd.setIsParam(True)

        if not Utils._isInstanceOfStr(node.rangeInit):
            node.rangeInit.setupEnvironment(self)
        
        if not Utils._isInstanceOfStr(node.rangeEnd):
            node.rangeEnd.setupEnvironment(self)

    # Value List
    def setupEnvironment_ValueList(self, node):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        map(self._setupValue, node.values)

    # Tuple List
    def setupEnvironment_TupleList(self, node):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        map(self._setupValue, node.values)

    # Value
    def setupEnvironment_Value(self, node):
        """
        Generate the MathProg code for the declaration of the variable of this value
        """
        node.value.setupEnvironment(self)

    # Variable
    def setupEnvironment_Variable(self, node):
        """
        Generate the MathProg code for the declaration of this variable
        """

        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)
            return

        self.varKey = node.variable.generateCode(self.codeGenerator)

        if self.varKey[0].isupper():
            node.setIsParam(True)

        if node.isSet:
            if not self.varKey in self.codeGenerator.Sets: # check if this set was not seen yet
                self.codeGenerator.Sets[self.varKey] = {}
                self.codeGenerator.Sets[self.varKey]["sub-indices"] = []

                if len(node.sub_indices) > 0:
                    for i in range(len(node.sub_indices)):
                        self.codeGenerator.Sets[self.varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1})

            self.Stm = self.codeGenerator.Sets
            self._checkSubIndices(node)

        elif node.isParam:
            if not self.varKey in self.codeGenerator.Params and not self.varKey in self.codeGenerator.Sets: # check if this param was not seen yet
                self.codeGenerator.Params[self.varKey] = {}
                self.codeGenerator.Params[self.varKey]["type"] = ""
                self.codeGenerator.Params[self.varKey]["sub-indices"] = []

                if len(node.sub_indices) > 0:
                    for i in range(len(node.sub_indices)):
                        self.codeGenerator.Params[self.varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1, "set": ""})

            self.Stm = self.codeGenerator.Params
            self._checkSubIndices(node)

        else:
            if not self.varKey in self.codeGenerator.Vars and not self.varKey in self.codeGenerator.Params and not self.varKey in self.codeGenerator.Sets: # check if this variable was not seen yet
                self.codeGenerator.Vars[self.varKey] = {}
                self.codeGenerator.Vars[self.varKey]["type"] = ""
                self.codeGenerator.Vars[self.varKey]["sub-indices"] = []

                if len(node.sub_indices) > 0:
                    for i in range(len(node.sub_indices)):
                        self.codeGenerator.Vars[self.varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1, "set": ""})

            self.Stm = self.codeGenerator.Vars
            self._checkSubIndices(node)

    def setupEnvironment_Number(self, node):
        if node.getIndice() == -1:
            return

        num = int(self._getCodeID(node))

        if num < self.Stm[self.varKey]["sub-indices"][node.getIndice()]["min"]:
            self.Stm[self.varKey]["sub-indices"][node.getIndice()]["min"] = num
        elif num > self.Stm[self.varKey]["sub-indices"][node.getIndice()]["max"]:
            self.Stm[self.varKey]["sub-indices"][node.getIndice()]["max"] = num

    def setupEnvironment_ID(self, node):
        self._setupEnvironment_SubIndice(node)
