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
from GenBelongsTo import *
from GenFirstStmtList import *
from GenFirstStmt import *
from GenSubIndicesByNameList import *
from GenSubIndicesByName import *
from CodeGenerationException import *
from GenDeclaration import *
from Constants import *
from DeclarationExpression import *

class CodeSetup:
    """ Visitor in the Visitor Pattern """

    def __init__(self, codeGenerator = None):
        self.codeGenerator = codeGenerator
        self.varKey = None
        self.curList = None
        self.stmtIndex = 0
        self.genFirstStmtList = GenFirstStmtList()
        self.genSubIndicesByNameList = GenSubIndicesByNameList()

    def _setIsParam(self, variable):
        variable.setIsParam(True)
        variable.setIsSet(False)

    def _setIsSet(self, variable):
        variable.setIsSet(True)
        variable.setIsParam(False)

    def setupEnvironment(self, node):
        cls = node.__class__
        method_name = 'setupEnvironment_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    # Auxiliary Methods
    def _getVariable(self, var):
        if isinstance(var, ValuedNumericExpression) or isinstance(var, StringSymbolicExpression) or isinstance(var, SetExpressionWithValue):
            var = var.value

        return var

    def _addTypeAux(self, variable, _type, minVal = None, maxVal = None):
        name = variable.generateCodeWithoutIndices(self.codeGenerator)
        self.codeGenerator.genTypes.add(GenType(name, _type, minVal, maxVal))

        if not self._checkIsParamType(_type):
            variable.setIsVar(True)
            variable.setIsParam(False)

            # if the parameter was included in the current statement, remove because it is not a parameter but an index
            _genParam = self.codeGenerator.genParameters.getByNameAndStmtInclusion(name, self.stmtIndex)
            if _genParam != None and len(_genParam) > 0:
                self.removeSavingFirstStmtAndSubIndicesForName(self.codeGenerator.genParameters, name)

        else:
            variable.setIsSymbolic(True)
            self._setIsParam(variable)

    def _addType(self, variable, _type, minVal = None, maxVal = None):
        if isinstance(variable, ValueList):
            for var in variable.getValues():
                var = self._getVariable(var)

                self._addTypeAux(var, _type, minVal, maxVal)
        else:
            var = self._getVariable(variable)

            self._addTypeAux(var, _type, minVal, maxVal)

    def _addDomainAux(self, variable, setExpression, setExpressionObj):
        ind = variable.generateCodeWithoutIndices(self.codeGenerator)
        _domains = self.codeGenerator.genDomains.getByNameAndStmt(ind, self.stmtIndex)

        order = 0
        if _domains != None and len(_domains) > 0:
            order = self._getOrderFromDomains(_domains)
            order += 1

        _domain = GenDomain(ind, self.stmtIndex, order, setExpression, setExpressionObj)
        self.codeGenerator.genDomains.add(_domain)

    def _addDomain(self, variable, setExpression, setExpressionObj):
        if isinstance(variable, ValueList):
            for var in variable.getValues():
                var = self._getVariable(var)

                self._addDomainAux(var, setExpression, setExpressionObj)

        else:
            var = self._getVariable(variable)
            self._addDomainAux(var, setExpression, setExpressionObj)

    def _checkIsParamType(self, _type):
        return _type.startswith(Constants.SYMBOLIC) or _type.startswith(Constants.LOGICAL)

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

    # Get the MathProg code for a given declaration
    def _setupDeclaration(self, declaration):
        declaration.setupEnvironment(self)
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
            var.setVarList(Constants.GEN_VARIABLES)
        elif isinstance(curList, GenSets):
            var.setVarList(Constants.GEN_SETS)
        elif isinstance(curList, GenParameters):
            var.setVarList(Constants.GEN_PARAMETERS)

    def _getCurList(self, node):
        curList = None
        if node.getVarList() == Constants.GEN_VARIABLES:
            curList = self.codeGenerator.genVariables
        elif node.getVarList() == Constants.GEN_PARAMETERS:
            curList = self.codeGenerator.genParameters
        elif node.getVarList() == Constants.GEN_SETS:
            curList = self.codeGenerator.genSets

        return curList

    def _getOrderFromDomains(self, _domains):
        order = -1
        for _d in _domains:
            if _d.getOrder() > order:
                order = _d.getOrder()

        return order

    def _checkSubIndices(self, node):
        if Utils._isInstanceOfStr(node.sub_indices):
            return

        if len(node.sub_indices) > 0:
            if Utils._isInstanceOfList(node.sub_indices):
                indices = range(len(node.sub_indices))
                for i in indices:
                    var = node.sub_indices[i]
                    var = self._getVariable(var)

                    self._setIndices(var, i, self.varKey, self.curList)

                for i in indices:
                    var = node.sub_indices[i]
                    var = self._getVariable(var)

                    var.setupEnvironment(self)

            elif isinstance(node.sub_indices, ValuedNumericExpression) or isinstance(node.sub_indices, StringSymbolicExpression):
                self._setIndices(node.sub_indices.value, 0, self.varKey, self.curList)
                node.sub_indices.value.setupEnvironment(self)

            else:
                self._setIndices(node.sub_indices, 0, self.varKey, self.curList)
                node.sub_indices.setupEnvironment(self)

    def _setupEnvironment_SubIndice(self, node):
        ind = node.generateCode(self.codeGenerator)
        _domains = self.codeGenerator.genDomains.getByNameAndStmt(ind, self.stmtIndex)
        order = 0
        if _domains != None and len(_domains) > 0:
            order = self._getOrderFromDomains(_domains)
            order += 1

        _domain = GenDomain(ind, self.stmtIndex, order)
        self.codeGenerator.genDomains.add(_domain)

        if node.getVarList() == None:
            return

        curList = self._getCurList(node)
        _genObj = None
        if curList != None:
            _genObj = curList.get(node.getVarName())

        if _genObj != None:
            orderSub = 0

            _subIndices = _genObj.getSubIndices()
            _subIndice = _subIndices.getByIndiceAndStmt(node.getIndice(), self.stmtIndex)

            if _subIndice != None and len(_subIndice) > 0:
                orderSub = self._getOrderFromDomains(_subIndice)
                orderSub += 1

            _subInd = GenSubIndice(node.getIndice(), ind, self.stmtIndex, orderSub, order, None, None, _subIndices)
            _subIndices.add(_subInd) # set the name of the variable as the index

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
        
        if node.declarations:
            node.declarations.setupEnvironment(self)

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
        node.numericExpression1.setupEnvironment(self)
        node.linearExpression.setupEnvironment(self)
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
            node.indexingExpression.setHasSup(True)
            node.indexingExpression.setSupExpression(node.numericExpression.generateCode(self.codeGenerator))
        
        node.indexingExpression.setupEnvironment(self)

        if node.numericExpression:
            node.numericExpression.setupEnvironment(self)

        node.linearExpression.setupEnvironment(self)
        

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

        if node.numericExpression1 != None:
            node.numericExpression1.setupEnvironment(self)

        if node.numericExpression2 != None:
            node.numericExpression2.setupEnvironment(self)

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
            node.indexingExpression.setHasSup(True)
            node.indexingExpression.setSupExpression(node.supNumericExpression.generateCode(self.codeGenerator))

        node.indexingExpression.setupEnvironment(self)
        
        if node.supNumericExpression:
            node.supNumericExpression.setupEnvironment(self)

        node.numericExpression.setupEnvironment(self)

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

        if node.symbolicExpression2 != None:
            node.symbolicExpression2.setupEnvironment(self)

    # Indexing Expression
    def setupEnvironment_IndexingExpression(self, node):
        """
        Generate the MathProg code for entries in this indexing expression
        """
        if node.hasSup:
            if len(node.entriesIndexingExpression) != 1:
                raise CodeGenerationException('Statement '+str(self.stmtIndex+1)+': If iterated expression has a superior expression, then it must have a single entry in the inferior expression!')
            #elif Utils._isInstanceOfStr(node.entriesIndexingExpression[0]) or not node.entriesIndexingExpression[0].isInstanceOfEntryIndexingExpressionEq():
            #    raise Exception('If iterated expression has a superior expression, then its single entry must be of type EntryIndexingExpressionEq!')
            else:
                node.entriesIndexingExpression[0].setHasSup(True)
                node.entriesIndexingExpression[0].setSupExpression(node.supExpression)

        map(self._setupEntry, node.entriesIndexingExpression)

        if node.logicalExpression:
            node.logicalExpression.setupEnvironment(self)

        if node.stmtIndexing:
            self.codeGenerator.genIndexingExpressionConstraints.add(GenIndexingExpression(str(self.stmtIndex), node.generateCode(self.codeGenerator)))

    def setupEnvironment_EntryExpressionWithSet(self, node, variable):

        if isinstance(variable, Variable):# and len(variable.sub_indices) > 0:
            variable.setupEnvironment(self)
        elif isinstance(variable, ValuedNumericExpression) or isinstance(variable, StringSymbolicExpression):
            variable.value.setupEnvironment(self)
        elif isinstance(variable, ValueList):
            for var in variable.getValues():
                var = self._getVariable(var)

                var.setupEnvironment(self)

        setExpression = node.setExpression.generateCode(self.codeGenerator)
        setCode = setExpression.replace(" ", "")

        if setCode == Constants.BINARY_0_1 or setCode == Constants.BINARY:
            node.isBinary = True
            self._addType(variable, Constants.BINARY)
            setExpression = Constants.BINARY_0_1

        elif setCode.startswith(Constants.INTEGER):
            node.isInteger = True
            self._addType(variable, setExpression)

        elif setCode.startswith(Constants.REALSET):
            node.isReal = True
            self._addType(variable, setExpression[8:], 0)

        elif setCode.startswith(Constants.SYMBOLIC):
            node.isSymbolic = True
            self._addType(variable, setExpression)

        elif setCode.startswith(Constants.LOGICAL):
            node.isLogical = True
            self._addType(variable, setExpression)

        self._addDomain(variable, setExpression, node.setExpression)

    def _setDimension(self, setExpression, dimen):

        if isinstance(setExpression, SetExpressionWithValue) or isinstance(setExpression, SetExpressionWithIndices):
            setExpression.setDimension(dimen)
        elif isinstance(setExpression, SetExpressionBetweenParenthesis):
            self._setDimension(setExpression.setExpression, dimen)
        elif isinstance(setExpression, ConditionalSetExpression) or isinstance(setExpression, SetExpressionWithOperation):
            self._setDimension(setExpression.setExpression1, dimen)
            self._setDimension(setExpression.setExpression2, dimen)

    def _addBelongsTo(self, var):
        var.setIsInSet(True)
        name = var.generateCode(self.codeGenerator)
        self.codeGenerator.genBelongsToList.add(GenBelongsTo(name, self.stmtIndex))

        # if the parameter was included in the current statement, remove because it is not a parameter but an index
        _genParam = self.codeGenerator.genParameters.getByNameAndStmtInclusion(name, self.stmtIndex)
        if _genParam != None and len(_genParam) > 0:
            self.removeSavingFirstStmtAndSubIndicesForName(self.codeGenerator.genParameters, name)

    def removeSavingFirstStmtAndSubIndicesForName(self, genList, name):
        objName = genList.get(name)
        if objName != None:
            genFirstStmt = self.genFirstStmtList.get(name)
            if genFirstStmt != None:
                genFirstStmt.setFirstStmt(objName.getFirstStmt())
            else:
                self.genFirstStmtList.add(GenFirstStmt(name, objName.getFirstStmt()))

            genSubIndicesByName = self.genSubIndicesByNameList.get(name)
            if genSubIndicesByName != None:
                _sub = objName.getSubIndices().getAll()
                genSubIndicesByName.getSubIndices().addAll(_sub)

            else:
                _subIndices = GenSubIndices()
                _sub = objName.getSubIndices().getAll()
                _subIndices.addAll(_sub)
                _subIndicesByName = GenSubIndicesByName(name)
                _subIndicesByName.setSubIndices(_subIndices)
                self.genSubIndicesByNameList.add(_subIndicesByName)

            genList.remove(name)

    # Entry Indexing Expression
    def setupEnvironment_EntryIndexingExpressionWithSet(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for indexing expression
        """

        if Utils._isInstanceOfStr(node.variable):
            return

        setExpression = node.setExpression.generateCode(self.codeGenerator)
        setCode = setExpression.replace(" ", "")

        if isinstance(node.variable, ValueList) or isinstance(node.variable, Tuple):
            for var in node.variable.getValues():
                var = self._getVariable(var)

                if not self._checkIsParamType(setCode) and len(var.sub_indices) == 0:
                    self._addBelongsTo(var)

        elif isinstance(node.variable, ValuedNumericExpression) or isinstance(node.variable, StringSymbolicExpression):
            if not self._checkIsParamType(setCode) and len(node.variable.value.sub_indices) == 0:
                self._addBelongsTo(node.variable.value)

        else:
            if not self._checkIsParamType(setCode) and len(node.variable.sub_indices) == 0:
                self._addBelongsTo(node.variable)

        if isinstance(node.variable, Tuple):
            tupleVal = node.variable.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                self._setDimension(node.setExpression, dimen)

            node.setExpression.setupEnvironment(self)

            self.codeGenerator.genTuples.add(GenTuple(
                node.setExpression.generateCode(self.codeGenerator), 
                map(lambda val: val.generateCode(self.codeGenerator), tupleVal), 
                node.op, self.stmtIndex, node.setExpression))

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
        _domains = self.codeGenerator.genDomains.getByNameAndStmt(ind, self.stmtIndex)

        order = 0
        if _domains != None and len(_domains) > 0:
            order = self._getOrderFromDomains(_domains)
            order += 1

        setExpression = node.value.generateCode(self.codeGenerator)
        if node.hasSup:
            setExpression += ".." + node.supExpression

        _domain = GenDomain(ind, self.stmtIndex, order, setExpression, node.value, node.supExpression if node.hasSup else None)
        self.codeGenerator.genDomains.add(_domain)

        if len(node.variable.sub_indices) == 0:
            self._addBelongsTo(node.variable)

        node.value.setupEnvironment(self)

        node.variable.setupEnvironment(self)

    def setupEnvironment_LogicalExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this numeric expression
        """
        map(self._setupEntryByKey, node.entriesLogicalExpression)

    # Entry Logical Expression
    def setupEnvironment_EntryLogicalExpressionNot(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        node.logicalExpression.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionNumericOrSymbolic(self, node):
        """
        Generate the MathProg code for the declaration of variables and sets used in this entry for logical expression
        """
        node.numericOrSymbolicExpression.setupEnvironment(self)

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

        setExpression = node.setExpression.generateCode(self.codeGenerator)
        setCode = setExpression.replace(" ", "")

        if isinstance(node.value, ValueList) or isinstance(node.value, Tuple):
            for var in node.value.getValues():
                var = self._getVariable(var)

                if not self._checkIsParamType(setCode) and len(var.sub_indices) == 0:
                    self._addBelongsTo(var)

        elif isinstance(node.value, ValuedNumericExpression) or isinstance(node.value, StringSymbolicExpression):
            if not self._checkIsParamType(setCode) and len(node.value.value.sub_indices) == 0:
                self._addBelongsTo(node.value.value)

        else:
            if not self._checkIsParamType(setCode) and len(node.value.sub_indices) == 0:
                self._addBelongsTo(node.value)

        if isinstance(node.value, Tuple):
            tupleVal = node.value.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                node.setExpression.setDimension(dimen)

            node.setExpression.setupEnvironment(self)

            self.codeGenerator.genTuples.add(GenTuple(
                node.setExpression.generateCode(self.codeGenerator), 
                map(lambda val: val.generateCode(self.codeGenerator), tupleVal), 
                node.op, self.stmtIndex, node.setExpression))

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

    def isParamForSure(self, var):
        if var.isParam:
            return True

        name = var.generateCodeWithoutIndices(self.codeGenerator)
        param = self.codeGenerator.genParameters.get(name)

        if param != None:
            return param.getCertainty()

        return False

    # Set Expression
    def setupEnvironment_SetExpressionWithValue(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        if not Utils._isInstanceOfStr(node.value):
            if isinstance(node.value, ValueList):
                for var in node.value.getValues():
                    var = self._getVariable(var)

                    if isinstance(var, Variable) and not self.isParamForSure(var):
                        self._setIsSet(var)

                    var.setupEnvironment(self)

            else:
                if isinstance(node.value, Variable) and not self.isParamForSure(node.value):
                    self._setIsSet(node.value)

                node.value.setupEnvironment(self)

    def setupEnvironment_SetExpressionWithIndices(self, node):
        """
        Generate the MathProg code for declaration of variables and sets used in this set expression
        """
        if len(node.indices) > 0:
            node.indices.setupEnvironment(self)

        if not Utils._isInstanceOfStr(node.variable):
            if isinstance(node.variable, Variable) and not self.isParamForSure(node.variable):
                self._setIsSet(node.variable)

            if len(node.indices) > 0:
                if isinstance(node.indices, Variable):
                    node.variable.setSubIndices([node.indices])
                elif isinstance(node.indices, ValuedNumericExpression) or isinstance(node.indices, StringSymbolicExpression):
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

    def setupEnvironment_SetExpressionBetweenBraces(self, node):
        """
        Generate the MathProg code for the variables and sets used in this set expression
        """
        if node.setExpression != None:
            node.setExpression.setupEnvironment(self)

    def setupEnvironment_IteratedSetExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this set expression
        """
        node.indexingExpression.setupEnvironment(self)

        if node.integrands != None and len(node.integrands) > 0:
            map(lambda el: el.setupEnvironment(self), node.integrands)

    def setupEnvironment_ConditionalSetExpression(self, node):
        """
        Generate the MathProg code for the variables and sets used in this set expression
        """
        node.logicalExpression.setupEnvironment(self)
        node.setExpression1.setupEnvironment(self)

        if node.setExpression2 != None:
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

        if node.by != None:
            node.by.setupEnvironment(self)
    
    # Value List
    def setupEnvironment_ValueList(self, node):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        map(self._setupValue, node.values)

    # Variable List
    def setupEnvironment_VariableList(self, node):
        """
        Generate the MathProg code for the declaration of variables used in this range expression
        """
        map(self._setupValue, node.variables)

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

            if len(node.sub_indices) == 0:
                return
        
        self.varKey = node.variable.generateCode(self.codeGenerator)
        
        self._setLastStmt(self.varKey, self.codeGenerator.genSets)
        self._setLastStmt(self.varKey, self.codeGenerator.genVariables)
        self._setLastStmt(self.varKey, self.codeGenerator.genParameters)

        if node.isVar or self.codeGenerator.genVariables.has(self.varKey):

            if not self.codeGenerator.genVariables.has(self.varKey): # check if this variable was not seen yet

                firstStmtShowed = None
                self.removeSavingFirstStmtAndSubIndicesForName(self.codeGenerator.genParameters, self.varKey)
                self.removeSavingFirstStmtAndSubIndicesForName(self.codeGenerator.genSets, self.varKey)
                firstStmt = self.genFirstStmtList.get(self.varKey)

                if firstStmt != None:
                    firstStmtShowed = firstStmt.getFirstStmt()
                
                _genVar = GenVariable(self.varKey, None, None, None, firstStmtShowed if firstStmtShowed != None else str(self.stmtIndex), str(self.stmtIndex))

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genVar)

                    _subIndicesByName = self.genSubIndicesByNameList.get(self.varKey)
                    if _subIndicesByName != None:
                        _subIndices.addAll(_subIndicesByName.getSubIndices().getAll())

                    _genVar.setSubIndices(_subIndices)

                self.codeGenerator.genVariables.add(_genVar)

            self.curList = self.codeGenerator.genVariables
            self._checkSubIndices(node)

        elif node.isSet:
            if not self.codeGenerator.genVariables.has(self.varKey) and not self.codeGenerator.genSets.has(self.varKey): # check if this variable was not seen yet
                firstStmtShowed = None
                self.removeSavingFirstStmtAndSubIndicesForName(self.codeGenerator.genParameters, self.varKey)
                firstStmt = self.genFirstStmtList.get(self.varKey)

                if firstStmt != None:
                    firstStmtShowed = firstStmt.getFirstStmt()

                _genSet = GenSet(self.varKey, node.dimenSet, firstStmtShowed if firstStmtShowed != None else str(self.stmtIndex), str(self.stmtIndex))

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genSet)
                    _genSet.setSubIndices(_subIndices)

                self.codeGenerator.genSets.add(_genSet)

            self.curList = self.codeGenerator.genSets
            self._checkSubIndices(node)

        elif not node.isInSet and not self.codeGenerator.genBelongsToList.has(GenBelongsTo(self.varKey, self.stmtIndex)):
            if not self.codeGenerator.genVariables.has(self.varKey) and not self.codeGenerator.genParameters.has(self.varKey): # check if this param was not seen yet
                firstStmtShowed = None
                self.removeSavingFirstStmtAndSubIndicesForName(self.codeGenerator.genSets, self.varKey)
                firstStmt = self.genFirstStmtList.get(self.varKey)

                if firstStmt != None:
                    firstStmtShowed = firstStmt.getFirstStmt()
                
                _genParam = GenParameter(self.varKey, node.isSymbolic or node.isLogical, firstStmtShowed if firstStmtShowed != None else str(self.stmtIndex), str(self.stmtIndex), str(self.stmtIndex))
                if node.isParam != None and not node.isParam:
                    _genParam.setCertainty(False)

                if len(node.sub_indices) > 0:
                    _subIndices = GenSubIndices(_genParam)

                    _subIndicesByName = self.genSubIndicesByNameList.get(self.varKey)
                    if _subIndicesByName != None:
                        _subIndices.addAll(_subIndicesByName.getSubIndices().getAll())

                    _genParam.setSubIndices(_subIndices)

                self.codeGenerator.genParameters.add(_genParam)
            elif node.isSymbolic or node.isLogical:
                _genParam = self.codeGenerator.genParameters.get(self.varKey)
                if _genParam != None:
                    _genParam.setIsSymbolic(True)

            self.curList = self.codeGenerator.genParameters
            self._checkSubIndices(node)

        else:
            if self.codeGenerator.genSets.has(self.varKey):
                self.curList = self.codeGenerator.genSets
            elif self.codeGenerator.genParameters.has(self.varKey):
                self.curList = self.codeGenerator.genParameters 
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
                order = self._getOrderFromDomains(_subIndice)
                order += 1

            _subIndice = GenSubIndice(node.getIndice(), num, self.stmtIndex, order, None, None, None, _subIndices)
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
                order = self._getOrderFromDomains(_subIndice)
                order += 1

            _subIndice = GenSubIndice(node.getIndice(), string, self.stmtIndex, order, None, None, None, _subIndices)
            _genObj.getSubIndices().add(_subIndice)

    # Declarations
    def setupEnvironment_Declarations(self, node):
        map(self._setupDeclaration, node.declarations)
    
    def setupEnvironment_Declaration(self, node):
        """
        Generate the MathProg code for declaration of variables and sets in this declaeation
        """
        #variables = node.declarationExpression.variables
        #var = self._getVariable(var)

        for var in node.declarationExpression.variables:
            var = self._getVariable(var)
            
            if isinstance(var, Variable):
                name = var.generateCodeWithoutIndices(self.codeGenerator)
                genDeclaration = self.codeGenerator.genDeclarations.get(name)

                if genDeclaration == None:
                    genDeclaration = GenDeclaration(name, list(node.declarationExpression.attributeList), None, str(self.stmtIndex))
                    self.codeGenerator.genDeclarations.add(genDeclaration)
                else:
                    genDeclaration.addAttributes(node.declarationExpression.attributeList)

                if node.indexingExpression and len(var.sub_indices) > 0:
                    genDeclaration.setIndexingExpression(node.indexingExpression)

        node.declarationExpression.setupEnvironment(self)

        if node.indexingExpression:
            node.indexingExpression.setupEnvironment(self)

    def setupEnvironment_DeclarationExpression(self, node):
        """
        Generate the MathProg code for the variables and sets in this declaration
        """
        #var = node.variable
        #var = self._getVariable(var)

        for var in node.variables:
            var = self._getVariable(var)

            if isinstance(var, Variable):
                var.setIsParam(False)

                name = var.generateCodeWithoutIndices(self.codeGenerator)
                if self.codeGenerator.genSets.has(name):
                    self._setIsSet(var)

                map(lambda el: self.setupEnvironment_AttributeListPre(el, var), node.attributeList)
                map(lambda el: self.setupEnvironment_AttributeList(el, var), node.attributeList)

        map(lambda el: el.setupEnvironment(self), node.attributeList)            

        for var in node.variables:
            var.setupEnvironment(self)

    def setupEnvironment_DeclarationAttribute(self, node):
        """
        Generate the MathProg code for the variables and sets in this declaration
        """
        node.attribute.setupEnvironment(self)

    def setupEnvironment_AttributeListPre(self, node, variable):
        if node.op == DeclarationAttribute.IN:
            self.setupEnvironment_DeclarationExpressionWithSet(node.attribute, variable)

        elif (node.op == DeclarationAttribute.ST or node.op == DeclarationAttribute.DF or node.op == DeclarationAttribute.WT) and isinstance(node.attribute, SetExpression) and (variable.isParam == None or not variable.isParam):
            var = self._getVariable(node.attribute)
            name = var.generateCode(self.codeGenerator)
            
            if not self.codeGenerator.genParameters.has(name):
                self._setIsSet(variable)

    def setupEnvironment_AttributeList(self, node, variable):
        var = self._getVariable(node.attribute)
        if (node.op == DeclarationAttribute.ST or node.op == DeclarationAttribute.DF) and variable.isParam != None and variable.isParam and isinstance(var, Variable):

            name = var.generateCodeWithoutIndices(self.codeGenerator)
            param = self.codeGenerator.genParameters.get(name)
            if param != None:
                param.setCertainty(True)

            self._setIsParam(var)

        #node.setupEnvironment(self)
        
    def setupEnvironment_DeclarationExpressionWithSet(self, attribute, variable):
        setExpression = attribute.generateCode(self.codeGenerator)

        #if isinstance(variable, Variable):# and len(variable.sub_indices) > 0:
        #    variable.setupEnvironment(self)
        #elif isinstance(variable, ValuedNumericExpression) or isinstance(variable, StringSymbolicExpression):
        #    variable.value.setupEnvironment(self)
        #elif isinstance(variable, ValueList):
        #    for var in variable.getValues():
        #        var = self._getVariable(var)

        #        var.setupEnvironment(self)

        setCode = setExpression.replace(" ", "")

        if setCode == Constants.BINARY_0_1 or setCode == Constants.BINARY:
            self._addType(variable, Constants.BINARY)
            setExpression = Constants.BINARY_0_1

        elif setCode.startswith(Constants.INTEGER):
            self._addType(variable, setExpression)

        elif setCode.startswith(Constants.REALSET):
            self._addType(variable, setExpression[8:], 0)

        elif setCode.startswith(Constants.SYMBOLIC):
            self._addType(variable, setExpression)
            
        elif setCode.startswith(Constants.LOGICAL):
            self._addType(variable, setExpression)

        self._addDomain(variable, setExpression, attribute)
