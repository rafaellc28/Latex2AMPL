from Utils import *
from TupleList import *
from ValueList import *
from Variable import *
from GenSubIndices import *
from GenSet import *
from GenSubIndice import *
from GenVariable import *
from GenParameter import *
from GenDomain import *
from GenType import *
from GenTuple import *

class CodeSetup:
    """ Visitor in the Visitor Pattern """

    def __init__(self, codeGenerator = None):
        self.codeGenerator = codeGenerator
        self.varKey = None
        self.curList = None

    def setupEnvironment(self, node):
        cls = node.__class__
        method_name = 'setupEnvironment_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    # Auxiliary Methods

    def _addTypeAux(self, variable, _type, minVal = None, maxVal = None):
        name = variable.generateCodeWithoutIndices(self.codeGenerator)
        self.codeGenerator.genTypes.add(GenType(name, _type, minVal, maxVal))
        self.codeGenerator.genParameters.remove(name)
        variable.setIsVar(True)
        variable.setIsParam(False)

    def _addType(self, variable, _type, minVal = None, maxVal = None):
        if isinstance(variable, ValueList):
            for var in variable.getValues():
                self._addTypeAux(var, _type, minVal, maxVal)
        else:
            self._addTypeAux(variable, _type, minVal, maxVal)

    def _addIndiceAux(self, variable, setExpression):
        ind = variable.generateCode(self.codeGenerator)
        _domain = self.codeGenerator.genDomains.get(ind)
        if _domain != None:
            _domain.setDomain(setExpression)

    def _addIndice(self, variable, setExpression):
            if isinstance(variable, ValueList):
                for var in variable.getValues():
                    self._addIndiceAux(var, setExpression)
            else:
                self._addIndiceAux(variable, setExpression)

    def _checkIsParam(self, strValue):
        return strValue[0].isupper()

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
        if not self.codeGenerator.genDomains.has(ind):
            self.codeGenerator.genDomains.add(GenDomain(ind))

        if self.curList == None:
            return
        
        _genObj = self.curList.get(self.varKey)
        if _genObj != None:
            _subIndices = _genObj.getSubIndices()

            if _subIndices.getByIndice(node.getIndice()) == None:
                _subIndices.add(GenSubIndice(node.getIndice(), ind, None, None, _subIndices)) # set the name of the variable as the index

    def setupEnvironment_Main(self, node):
        node.problem.setupEnvironment(self)

    # Linear Equations
    def setupEnvironment_LinearEquations(self, node):
        """
        Generate the MathProg code for the Set, Parameter and Variable statements
        """
        node.constraints.setupEnvironment(self)

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

        setExpression = node.setExpression.generateCode(self.codeGenerator)
        setCode = setExpression.replace(" ", "")

        if setCode == "{0,1}" or setCode == "binary":
            node.isBinary = True
            self._addType(variable, "binary")
            setExpression = "{0,1}"

        elif setCode.startswith("integer"):
            node.isInteger = True
            self._addType(variable, setExpression)

        elif setCode.startswith("realset"):
            node.isReal = True
            self._addType(variable, setExpression[8:], 0)

        self._addIndice(variable, setExpression)

    # Entry Indexing Expression
    def setupEnvironment_EntryIndexingExpressionWithSet(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for indexing expression
        """

        if Utils._isInstanceOfStr(node.variable):
            return

        if isinstance(node.variable, TupleList):
            tupleVal = node.variable.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                node.setExpression.setDimension(dimen)

            node.setExpression.setupEnvironment(self)
            self.codeGenerator.genTuples.add(GenTuple(
                node.setExpression.generateCode(self.codeGenerator), 
                map(lambda val: val.generateCode(self.codeGenerator), tupleVal), 
                node.op))

        else:
            node.setExpression.setupEnvironment(self)
            self.setupEnvironment_EntryExpressionWithSet(node, node.variable)

        node.variable.setupEnvironment(self)
        

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
        _domain = self.codeGenerator.genDomains.get(ind)
        if _domain != None:
            _domain.setDomain(node.value.generateCode(self.codeGenerator))

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

        

        if isinstance(node.value, TupleList):
            tupleVal = node.value.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                node.setExpression.setDimension(dimen)

            node.setExpression.setupEnvironment(self)
            self.codeGenerator.genTuples.add(GenTuple(
                node.setExpression.generateCode(self.codeGenerator), 
                map(lambda val: val.generateCode(self.codeGenerator), tupleVal), 
                node.op))

        else:
            node.setExpression.setupEnvironment(self)
            self.setupEnvironment_EntryExpressionWithSet(node, node.value)
        
        node.value.setupEnvironment(self)
        

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
        if len(node.indices) > 0:
            node.indices.setupEnvironment(self)

        if not Utils._isInstanceOfStr(node.variable):
            node.variable.setIsSet(True)
            if len(node.indices) > 0:
                if isinstance(node.indices, Variable):
                    node.variable.setSubIndices([node.indices])
                else:
                    node.variable.setSubIndices(node.indices.getValues())

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

        if not node.isVar and self._checkIsParam(self.varKey):
            node.setIsParam(True)

        if node.isSet:
            if not self.codeGenerator.genSets.has(self.varKey): # check if this set was not seen yet
                _genSet = GenSet(self.varKey, node.dimenSet)
                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genSet)
                    _genSet.setSubIndices(_subIndices)
                    #for i in range(len(self.sub_indices)):
                    #    Sets[varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1})

                self.codeGenerator.genSets.add(_genSet)

            self.curList = self.codeGenerator.genSets
            self._checkSubIndices(node)

        elif node.isParam:
            if not self.codeGenerator.genVariables.has(self.varKey) and not self.codeGenerator.genParameters.has(self.varKey) and not self.codeGenerator.genSets.has(self.varKey): # check if this param was not seen yet
                _genParam = GenParameter(self.varKey)

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genParam)
                    _genParam.setSubIndices(_subIndices)
                    #for i in range(len(node.sub_indices)):
                    #    self.codeGenerator.genParameters[self.varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1, "set": ""})

                self.codeGenerator.genParameters.add(_genParam)

            self.curList = self.codeGenerator.genParameters
            self._checkSubIndices(node)

        elif node.isVar:
            if not self.codeGenerator.genVariables.has(self.varKey) and not self.codeGenerator.genParameters.has(self.varKey) and not self.codeGenerator.genSets.has(self.varKey): # check if this variable was not seen yet
                _genVar = GenVariable(self.varKey)

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genVar)
                    _genVar.setSubIndices(_subIndices)
                    #for i in range(len(node.sub_indices)):
                    #    self.codeGenerator.genVariables[self.varKey]["sub-indices"].append({"var": "", "min": float('inf'), "max": 1, "set": ""})

                self.codeGenerator.genVariables.add(_genVar)

            self.curList = self.codeGenerator.genVariables
            self._checkSubIndices(node)
        else:
            self.curList = self.codeGenerator.genVariables
            self._checkSubIndices(node)

        self.varKey = None
        self.curList = None

    def setupEnvironment_Number(self, node):
        if node.getIndice() == -1 or self.curList == None:
            return

        num = int(self._getCodeID(node))
        _genObj = self.curList.get(self.varKey)

        if _genObj != None:
            _subIndice = _genObj.getSubIndices().getByIndice(node.getIndice())

            if _subIndice == None:
                _subIndice = GenSubIndice(node.getIndice(), num, None, None, _genObj.getSubIndices())
                _genObj.getSubIndices().add(_subIndice)

            if num < _subIndice.getMinVal():
                _subIndice.setMinVal(num)
            elif num > _subIndice.getMaxVal():
                _subIndice.setMaxVal(num)

    def setupEnvironment_ID(self, node):
        self._setupEnvironment_SubIndice(node)

    def setupEnvironment_String(self, node):
        pass
