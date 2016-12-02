from Utils import *
from Tuple import *
from ValueList import *
from Variable import *
from String import *
from SetExpression import *
from NumericExpression import *
from SymbolicExpression import *
from GenSubIndices import *
from GenSet import *
from GenSubIndice import *
from GenVariable import *
from GenParameter import *
from GenDomain import *
from GenType import *
from GenTuple import *
from GenIndexingExpression import *
from GenVariables import *
from GenSets import *
from GenParameters import *

class CodeSetup:
    """ Visitor in the Visitor Pattern """

    def __init__(self, codeGenerator = None):
        self.codeGenerator = codeGenerator
        self.varKey = None
        self.curList = None
        self.stmtIndex = 0

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

        if _type != "symbolic":
            variable.setIsVar(True)
            variable.setIsParam(False)
        else:
            variable.setIsSymbolic(True)

    def _addType(self, variable, _type, minVal = None, maxVal = None):
        if isinstance(variable, ValueList):
            for var in variable.getValues():
                if isinstance(var, ValuedNumericExpression):
                    var = var.value

                self._addTypeAux(var, _type, minVal, maxVal)
        else:
            var = variable
            if isinstance(var, ValuedNumericExpression):
                var = var.value

            self._addTypeAux(var, _type, minVal, maxVal)

    def _addDomainAux(self, variable, setExpression):
        ind = variable.generateCode(self.codeGenerator)
        _domain = self.codeGenerator.genDomains.get(GenDomain(ind, self.stmtIndex))
        if _domain == None:
            _domain = GenDomain(ind, self.stmtIndex)
            self.codeGenerator.genDomains.add(_domain)

        _domain.setDomain(setExpression)

    def _addDomain(self, variable, setExpression):
        if isinstance(variable, ValueList):
            for var in variable.getValues():
                if isinstance(var, ValuedNumericExpression):
                    var = var.value

                self._addDomainAux(var, setExpression)

        else:
            var = variable
            if isinstance(var, ValuedNumericExpression):
                var = var.value

            self._addDomainAux(var, setExpression)

    def _checkIsParam(self, strValue):
        return strValue[0].isupper()

    # Get the MathProg code for a given sub-indice
    def _getCodeID(self, id_):
        val = id_.generateCode(self.codeGenerator)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given objective
    def _setupObjective(self, objective):
        objective.setupEnvironment(self)
        self.stmtIndex += 1

    # Get the MathProg code for a given constraint
    def _setupConstraint(self, constraint):
        constraint.setupEnvironment(self)
        self.stmtIndex += 1

    # Get the MathProg code for a given constraint
    def _setupEntry(self, entry): return entry.setupEnvironment(self)

    # Get the MathProg code for a given entry
    def _setupEntryByKey(self, entry):
        for key in entry:
            return entry[key].setupEnvironment(self)

    def _setupValue(self, value):
        value.setupEnvironment(self)

    def _setIndices(self, var, i, varKey, curList):
        var.setIndice(i)
        var.setVarName(varKey)

        if isinstance(curList, GenVariables):
            var.setVarList("GenVariables")
        elif isinstance(curList, GenSets):
            var.setVarList("GenSets")
        elif isinstance(curList, GenParameters):
            var.setVarList("GenParameters")

    def _getCurList(self, node):
        curList = None
        if node.getVarList() == "GenVariables":
            curList = self.codeGenerator.genVariables
        elif node.getVarList() == "GenParameters":
            curList = self.codeGenerator.genParameters
        elif node.getVarList() == "GenSets":
            curList = self.codeGenerator.genSets

        return curList

    def _checkSubIndices(self, node):
        if Utils._isInstanceOfStr(node.sub_indices):
            return 

        if len(node.sub_indices) > 0:
            if Utils._isInstanceOfList(node.sub_indices):
                indices = range(len(node.sub_indices))
                for i in indices:
                    var = node.sub_indices[i]

                    if isinstance(var, ValuedNumericExpression) or isinstance(var, StringSymbolicExpression):
                        var = var.value

                    self._setIndices(var, i, self.varKey, self.curList)

                for i in indices:
                    var = node.sub_indices[i]

                    if isinstance(var, ValuedNumericExpression) or isinstance(var, StringSymbolicExpression):
                        var = var.value

                    var.setupEnvironment(self)

            elif isinstance(node.sub_indices, ValuedNumericExpression) or isinstance(node.sub_indices, StringSymbolicExpression):
                self._setIndices(node.sub_indices.value, 0, self.varKey, self.curList)
                node.sub_indices.value.setupEnvironment(self)

            else:
                self._setIndices(node.sub_indices, 0, self.varKey, self.curList)
                node.sub_indices.setupEnvironment(self)

    def _setupEnvironment_SubIndice(self, node):
        ind = node.generateCode(self.codeGenerator)
        self.codeGenerator.genDomains.add(GenDomain(ind, self.stmtIndex))

        if node.getVarList() == None:
            return

        curList = self._getCurList(node)
        _genObj = None
        if curList != None:
            _genObj = curList.get(node.getVarName())

        if _genObj != None:
            order = 0

            _subIndices = _genObj.getSubIndices()
            _subIndice = _subIndices.getByIndiceAndStmt(node.getIndice(), self.stmtIndex)

            if _subIndice != None and len(_subIndice) > 0:
                for idx in _subIndice:
                    if idx.getOrder() > order:
                        order = idx.getOrder()

                order += 1

            _subIndices.add(GenSubIndice(node.getIndice(), ind, self.stmtIndex, order, None, None, _subIndices)) # set the name of the variable as the index


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

    # Objectives
    def setupEnvironment_Objectives(self, node):
        """
        Generate the MathProg code for the variables and sets used in these objectives
        """
        map(self._setupObjective, node.objectives)

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

    def setupEnvironment_ConditionalLinearExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this linear expression
        """
        node.logicalExpression.setupEnvironment(self)
        node.linearExpression1.setupEnvironment(self)
        if node.linearExpression2 != None:
            node.linearExpression2.setupEnvironment(self)

    # Numeric Expression
    def setupEnvironment_NumericExpressionWithFunction(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_ValuedNumericExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.value.setupEnvironment(self)

    def setupEnvironment_NumericExpressionBetweenParenthesis(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_NumericExpressionWithArithmeticOperation(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.numericExpression1.setupEnvironment(self)
        node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_MinusNumericExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_IteratedNumericExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        if node.supNumericExpression:
            node.supNumericExpression.setupEnvironment(self)
            node.indexingExpression.setHasSup(True)
        
        node.numericExpression.setupEnvironment(self)
        node.indexingExpression.setupEnvironment(self)

    def setupEnvironment_ConditionalNumericExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.logicalExpression.setupEnvironment(self)
        node.numericExpression1.setupEnvironment(self)
        if node.numericExpression2 != None:
            node.numericExpression2.setupEnvironment(self)


    # Symbolic Expression
    def setupEnvironment_SymbolicExpressionWithFunction(self, node):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.symbolicExpression.setupEnvironment(self)
        node.numericExpression1.setupEnvironment(self)
        if node.numericExpression2 != None:
            node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_StringSymbolicExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.value.setupEnvironment(self)

    def setupEnvironment_SymbolicExpressionBetweenParenthesis(self, node):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.symbolicExpression.setupEnvironment(self)

    def setupEnvironment_SymbolicExpressionWithOperation(self, node):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.symbolicExpression1.setupEnvironment(self)
        node.symbolicExpression2.setupEnvironment(self)

    def setupEnvironment_ConditionalSymbolicExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this symbolic expression
        """
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)

        node.logicalExpression.setupEnvironment(self)
        node.symbolicExpression1.setupEnvironment(self)
        node.symbolicExpression2.setupEnvironment(self)

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

        if node.stmtIndexing:
            self.codeGenerator.genIndexingExpressionConstraints.add(GenIndexingExpression(str(self.stmtIndex), node.generateCode(self.codeGenerator)))

    def setupEnvironment_EntryExpressionWithSet(self, node, variable):
        if isinstance(variable, Variable):# and len(variable.sub_indices) > 0:
            variable.setupEnvironment(self)
        elif isinstance(variable, ValuedNumericExpression):
            variable.value.setupEnvironment(self)
        elif isinstance(variable, ValueList):
            for var in variable.getValues():
                #if len(var.sub_indices) > 0:
                if isinstance(var, ValuedNumericExpression):
                    var = var.value

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
        elif setCode.startswith("symbolic"):
            node.isSymbolic = True
            self._addType(variable, setExpression)

        self._addDomain(variable, setExpression)

    def _setDimension(self, setExpression, dimen):

        if isinstance(setExpression, SetExpressionWithValue) or isinstance(setExpression, SetExpressionWithIndices):
            setExpression.setDimension(dimen)
        elif isinstance(setExpression, SetExpressionBetweenParenthesis):
            self._setDimension(setExpression.setExpression, dimen)
        elif isinstance(setExpression, ConditionalSetExpression) or isinstance(setExpression, SetExpressionWithOperation):
            self._setDimension(setExpression.setExpression1, dimen)
            self._setDimension(setExpression.setExpression2, dimen)


    # Entry Indexing Expression
    def setupEnvironment_EntryIndexingExpressionWithSet(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for indexing expression
        """

        if Utils._isInstanceOfStr(node.variable):
            return

        if isinstance(node.variable, Tuple):
            tupleVal = node.variable.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                self._setDimension(node.setExpression, dimen)

            node.setExpression.setupEnvironment(self)

            self.codeGenerator.genTuples.add(GenTuple(
                node.setExpression.generateCode(self.codeGenerator), 
                map(lambda val: val.generateCode(self.codeGenerator), tupleVal), 
                node.op, self.stmtIndex))

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
        _domain = self.codeGenerator.genDomains.get(GenDomain(ind, self.stmtIndex))
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

        if isinstance(node.value, Tuple):
            tupleVal = node.value.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                node.setExpression.setDimension(dimen)

            node.setExpression.setupEnvironment(self)

            self.codeGenerator.genTuples.add(GenTuple(
                node.setExpression.generateCode(self.codeGenerator), 
                map(lambda val: val.generateCode(self.codeGenerator), tupleVal), 
                node.op, self.stmtIndex))

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
            if isinstance(node.value, ValueList):
                for var in node.value.getValues():
                    if isinstance(var, ValuedNumericExpression):
                        var = var.value

                    if isinstance(var, Variable) and not self.codeGenerator.genParameters.has(var.generateCode(self.codeGenerator)):
                        var.setIsSet(True)

                    var.setupEnvironment(self)

            else:
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
                elif isinstance(node.indices, ValuedNumericExpression):
                    node.variable.setSubIndices([node.indices.value])
                else:
                    node.variable.setSubIndices(node.indices.getValues())

            node.variable.setupEnvironment(self)

    def setupEnvironment_SetExpressionWithOperation(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        node.setExpression1.setupEnvironment(self)
        node.setExpression2.setupEnvironment(self)

    def setupEnvironment_SetExpressionBetweenParenthesis(self, node):
        """
        Generate the MathProg code for the variables and sets used in this set expression
        """
        node.setExpression.setupEnvironment(self)

    def setupEnvironment_ConditionalSetExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this set expression
        """
        node.logicalExpression.setupEnvironment(self)
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

    # Tuple
    def setupEnvironment_Tuple(self, node):
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

    def _setLastStmt(self, name, genList):
        _genObj = genList.get(name)
        if _genObj != None:
            if int(_genObj.getLastStmt()) < self.stmtIndex:
                _genObj.setLastStmt(str(self.stmtIndex))


    # Variable
    def setupEnvironment_Variable(self, node):
        """
        Generate the MathProg code for the declaration of this variable
        """
        
        if node.getIndice() > -1:
            self._setupEnvironment_SubIndice(node)
            return
        
        self.varKey = node.variable.generateCode(self.codeGenerator)
        
        if not node.isVar and not node.isSet and self._checkIsParam(self.varKey):
            node.setIsParam(True)

        self._setLastStmt(self.varKey, self.codeGenerator.genSets)
        self._setLastStmt(self.varKey, self.codeGenerator.genVariables)
        self._setLastStmt(self.varKey, self.codeGenerator.genParameters)

        if node.isVar or self.codeGenerator.genVariables.has(self.varKey):
            self.codeGenerator.genParameters.remove(self.varKey)
            self.codeGenerator.genSets.remove(self.varKey)

            if not self.codeGenerator.genVariables.has(self.varKey): # check if this variable was not seen yet
                _genVar = GenVariable(self.varKey, None, None, None, str(self.stmtIndex), str(self.stmtIndex))

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genVar)
                    _genVar.setSubIndices(_subIndices)

                self.codeGenerator.genVariables.add(_genVar)

            self.curList = self.codeGenerator.genVariables
            self._checkSubIndices(node)

        elif node.isSet:
            if not self.codeGenerator.genVariables.has(self.varKey) and not self.codeGenerator.genParameters.has(self.varKey) and not self.codeGenerator.genSets.has(self.varKey): # check if this variable was not seen yet
                _genSet = GenSet(self.varKey, node.dimenSet, str(self.stmtIndex), str(self.stmtIndex))

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genSet)
                    _genSet.setSubIndices(_subIndices)

                self.codeGenerator.genSets.add(_genSet)

            self.curList = self.codeGenerator.genSets
            self._checkSubIndices(node)

        elif node.isParam:
            self.codeGenerator.genSets.remove(self.varKey)
            if not self.codeGenerator.genVariables.has(self.varKey) and not self.codeGenerator.genParameters.has(self.varKey): # check if this param was not seen yet
                _genParam = GenParameter(self.varKey, node.isSymbolic, str(self.stmtIndex), str(self.stmtIndex))

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genParam)
                    _genParam.setSubIndices(_subIndices)

                self.codeGenerator.genParameters.add(_genParam)

            self.curList = self.codeGenerator.genParameters
            self._checkSubIndices(node)

        else:
            self.curList = self.codeGenerator.genVariables
            self._checkSubIndices(node)

        self.varKey = None
        self.curList = None

    def setupEnvironment_Number(self, node):
        if node.getIndice() == -1 or node.getVarList() == None:
            return

        curList = self._getCurList(node)

        _genObj = None
        if curList != None:
            _genObj = curList.get(node.getVarName())

        if _genObj != None:
            num = int(self._getCodeID(node))
            order = 0

            _subIndices = _genObj.getSubIndices()
            _subIndice = _subIndices.getByIndiceAndStmt(node.getIndice(), self.stmtIndex)

            if _subIndice != None and len(_subIndice) > 0:
                for idx in _subIndice:
                    if idx.getOrder() > order:
                        order = idx.getOrder()

                order += 1

            _subIndice = GenSubIndice(node.getIndice(), num, self.stmtIndex, order, None, None, _subIndices)
            _genObj.getSubIndices().add(_subIndice)

            if num < _subIndice.getMinVal():
                _subIndice.setMinVal(num)
            elif num > _subIndice.getMaxVal():
                _subIndice.setMaxVal(num)

    def setupEnvironment_ID(self, node):
        self._setupEnvironment_SubIndice(node)

    def setupEnvironment_String(self, node):
        if node.getIndice() == -1 or node.getVarList() == None:
            return

        curList = self._getCurList(node)

        _genObj = None
        if curList != None:
            string = node.string
            _genObj = curList.get(node.getVarName())

        if _genObj != None:
            order = 0

            _subIndices = _genObj.getSubIndices()
            _subIndice = _subIndices.getByIndiceAndStmt(node.getIndice(), self.stmtIndex)

            if _subIndice != None and len(_subIndice) > 0:
                for idx in _subIndice:
                    if idx.getOrder() > order:
                        order = idx.getOrder()

                order += 1

            _subIndice = GenSubIndice(node.getIndice(), string, self.stmtIndex, order, None, None, _subIndices)
            _genObj.getSubIndices().add(_subIndice)
