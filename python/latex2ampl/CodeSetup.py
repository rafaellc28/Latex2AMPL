from Tuple import *
from ValueList import *
from Identifier import *
from SetExpression import *
from Range import *
from EntryIndexingExpression import *
from GenSet import *
from GenVariable import *
from GenParameter import *
from GenVariables import *
from GenSets import *
from GenParameters import *
from GenBelongsTo import *
from CodeGenerationException import *
from GenDeclaration import *
from GenProperties import *
from GenItemDomain import *
from Constants import *
from DeclarationExpression import *
from Declarations import *

from IntegerSet import *
from RealSet import *
from SymbolicSet import *
from LogicalSet import *
from BinarySet import *
from ParameterSet import *
from VariableSet import *
from SetSet import *

from SymbolTable import *
from SymbolTableEntry import *

class CodeSetup:
    """ Visitor in the Visitor Pattern """

    def __init__(self, codeGenerator = None):
        self.codeGenerator = codeGenerator
        self.identifier = None
        self.identifierKey = None
        self.stmtIndex = 0
        self.level = 0
        self.currentTable = None

    def _setIsParam(self, identifier):
        identifier.setIsParam(True)
        identifier.setIsSet(False)
        identifier.setIsVar(False)

    def _setIsSet(self, identifier):
        identifier.setIsSet(True)
        identifier.setIsParam(False)
        identifier.setIsVar(False)

    def _setIsVar(self, identifier):
        identifier.setIsVar(True)
        identifier.setIsSet(False)
        identifier.setIsParam(False)

    def setupEnvironment(self, node):
        cls = node.__class__
        method_name = 'setupEnvironment_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    # Auxiliary Methods
    def _getIdentifier(self, var):
        return var.getSymbol()

    def _addTypeAux(self, identifier, _type):
        name = identifier.getSymbolName(self.codeGenerator)

        if not self._checkIsModifierSet(_type):
            self._setIsVar(identifier)

            # if the parameter was included in the current statement, remove because it is not a parameter but an index
            _genParam = self.codeGenerator.genParameters.getByNameAndStmtInclusion(name, self.stmtIndex)
            if _genParam != None and len(_genParam) > 0:
                if not self.isParamForSure(identifier):
                    self.codeGenerator.genParameters.remove(name)
    
    def _addType(self, identifier, _type):
        if isinstance(identifier, ValueList):
            for var in identifier.getValues():
                var = self._getIdentifier(var)

                self._addTypeAux(var, _type)
        else:
            var = self._getIdentifier(identifier)
            self._addTypeAux(var, _type)

    def _checkIsModifierSet(self, _type):
        return isinstance(_type, SymbolicSet) or isinstance(_type, LogicalSet)

    def _getSetExpressionObj(self, value):
        setExpressionObj = value
        if isinstance(value, SetExpressionWithValue):
            setExpressionObj = value.value

        setExpression = setExpressionObj.getSymbolName(self.codeGenerator)
        setCode = setExpression.replace(" ", "")

        if setCode == Constants.BINARY_0_1 and not isinstance(setExpressionObj, BinarySet):
            setExpressionObj = BinarySet()

        return setExpressionObj

    def _getSetExpression(self, value):
        setExpression = value.getSymbolName(self.codeGenerator)
        setCode = setExpression.replace(" ", "")

        if setCode == Constants.BINARY_0_1:
            setExpression = Constants.BINARY_0_1

        return setExpression

    # Get the AMPL code for a given objective
    def _setupObjective(self, objective):
        self.level = 0
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex), self.level)

        objective.setupEnvironment(self)
        self.stmtIndex += 1
        self.currentTable = None

    # Get the AMPL code for a given declaration
    def _setupDeclaration(self, declaration):
        declaration.setupEnvironment(self)

    # Get the AMPL code for a given constraint
    def _setupConstraint(self, constraint):
        self.level = 0

        if not isinstance(constraint, Declarations) and not isinstance(constraint, Declaration):
            self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex), self.level)
        else:
            self.currentTable = None

        constraint.setupEnvironment(self)
        self.stmtIndex += 1
        self.currentTable = None

    # Get the AMPL code for a given constraint
    def _setupEntry(self, entry): return entry.setupEnvironment(self)

    # Get the AMPL code for a given entry
    def _setupEntryByKey(self, entry):
        for key in entry:
            return entry[key].setupEnvironment(self)

    def _setupValue(self, value):
        value.setupEnvironment(self)

    def _setIndices(self, var, i, varKey):
        var.setIndice(i)
        var.setIdentifierName(varKey)

    def _checkSubIndices(self, node):
        if isinstance(node.sub_indices, str):
            return

        if len(node.sub_indices) > 0:
            if isinstance(node.sub_indices, list):
                indices = range(len(node.sub_indices))
                for i in indices:
                    var = node.sub_indices[i]
                    var = self._getIdentifier(var)

                    self._setIndices(var, i, self.identifierKey)

                for i in indices:
                    var = node.sub_indices[i]
                    var = self._getIdentifier(var)

                    var.setupEnvironment(self)

            else:
                var = self._getIdentifier(node.sub_indices)
                self._setIndices(var, 0, self.identifierKey)
                var.setupEnvironment(self)

    def _setDimension(self, setExpression, dimen):
        if isinstance(setExpression, SetExpressionWithValue) or isinstance(setExpression, SetExpressionWithIndices):
            setExpression.setDimension(dimen)
        elif isinstance(setExpression, SetExpressionBetweenParenthesis):
            self._setDimension(setExpression.setExpression, dimen)
        elif isinstance(setExpression, ConditionalSetExpression) or isinstance(setExpression, SetExpressionWithOperation):
            self._setDimension(setExpression.setExpression1, dimen)
            self._setDimension(setExpression.setExpression2, dimen)

    def _addItemBelongsTo(self, var, name):
        if len(var.sub_indices) == 0:
            var.setIsInSet(True)
            self.codeGenerator.genBelongsToList.add(GenBelongsTo(name, self.stmtIndex))

            # if the parameter was included in the current statement, remove because it is not a parameter but an index
            _genParam = self.codeGenerator.genParameters.getByNameAndStmtInclusion(name, self.stmtIndex)
            if _genParam != None and len(_genParam) > 0:
                if not self.isDeclaredAsParam(var):
                    self.codeGenerator.genParameters.remove(name)

    def _addBelongsTo(self, var, setExpressionNode, op = None, supExpressionObj = None):
        self._addDomainExpression(var, setExpressionNode, op, supExpressionObj)

        if isinstance(var, Tuple):
            for var1 in var.getValues():
                name1 = var1.getSymbolName(self.codeGenerator)
                self._addItemBelongsTo(var1, name1)

        else:
            name = var.getSymbolName(self.codeGenerator)
            self._addItemBelongsTo(var, name)

    def _addDomainExpression(self, var, setExpressionNode, op = None, supExpressionObj = None):

        name = var.getSymbolName(self.codeGenerator)
        setExpression = self._getSetExpression(setExpressionNode)
        setExpressionObj = self._getSetExpressionObj(setExpressionNode)
        dependencies = setExpressionNode.getDependencies(self.codeGenerator)

        if supExpressionObj != None:
            setExpression += ".." + supExpressionObj.getSymbolName(self.codeGenerator)
            dependencies = list(set(dependencies + supExpressionObj.getDependencies(self.codeGenerator)))

        _symbolTableEntry = self.currentTable.lookup(name)
        if _symbolTableEntry == None:
            _symbolTableEntry = SymbolTableEntry(name, var, GenProperties(name, [GenItemDomain(setExpression, op, dependencies, setExpressionObj)], setExpressionNode.getDimension(), None, None), 
                                                 None, self.level, [])
            self.currentTable.insert(name, _symbolTableEntry)

        else:
            if _symbolTableEntry.getInferred():
                _symbolTableEntry.setType(None)

            _symbolTableEntry.getProperties().addDomain(GenItemDomain(setExpression, op, dependencies, setExpressionObj))
            _symbolTableEntry.getProperties().setDimension(setExpressionNode.getDimension())

        _symbolTableEntry = self.currentTable.lookup(setExpression)
        if _symbolTableEntry == None:
            _symbolTableEntry = SymbolTableEntry(setExpression, setExpressionNode, GenProperties(setExpression, [], setExpressionNode.getDimension(), None, None), 
                                                 None, self.level, [])
            self.currentTable.insert(setExpression, _symbolTableEntry)

        else:
            if _symbolTableEntry.getInferred():
                _symbolTableEntry.setType(None)

            _symbolTableEntry.getProperties().setDimension(setExpressionNode.getDimension())

    def isParamForSure(self, identifier):
        if identifier.isDeclaredAsParam:
            return True

        name = identifier.getSymbolName(self.codeGenerator)
        param1 = self.codeGenerator.genParameters.get(name)
        if param1 != None:
            return param1.getCertainty() or param1.getIsDeclaredAsParam()

        return False

    def isDeclaredAsParam(self, identifier):
        if identifier.isDeclaredAsParam:
            return True

        name = identifier.getSymbolName(self.codeGenerator)
        param1 = self.codeGenerator.genParameters.get(name)
        if param1 != None:
            return param1.getIsDeclaredAsParam()

        return False

    def isDeclaredAsSet(self, identifier):
        if identifier.isDeclaredAsSet:
            return True

        name = identifier.getSymbolName(self.codeGenerator)
        set1 = self.codeGenerator.genSets.get(name)

        if set1 != None:
            return set1.getIsDeclaredAsSet()

        return False

    def isDeclaredAsVar(self, identifier):
        if identifier.isDeclaredAsVar:
            return True
        
        name = identifier.getSymbolName(self.codeGenerator)
        var1 = self.codeGenerator.genVariables.get(name)

        if var1 != None:
            return var1.getIsDeclaredAsVar()

        return False

    def setupEnvironment_Main(self, node):
        node.problem.setupEnvironment(self)

    # Linear Equations
    def setupEnvironment_LinearEquations(self, node):
        """
        Generate the AMPL code for the Set, Parameter and Identifier statements
        """
        node.constraints.setupEnvironment(self)

    # Linear Program
    def setupEnvironment_LinearProgram(self, node):
        """
        Generate the AMPL code for the Set, Parameter and Identifier statements
        """
        
        node.objectives.setupEnvironment(self)
        if node.constraints:
            node.constraints.setupEnvironment(self)
        
    # Objectives
    def setupEnvironment_Objectives(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in these objectives
        """
        map(self._setupObjective, node.objectives)

    # Objective
    def setupEnvironment_Objective(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this objective function
        """
        node.linearExpression.setupEnvironment(self)

        if node.domain:
            node.domain.setupEnvironment(self)

    # Constraints
    def setupEnvironment_Constraints(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in these constraints
        """
        map(self._setupConstraint, node.constraints)

    # Constraint
    def setupEnvironment_Constraint(self, node):
        """
        Generate the AMPL code for declaration of identifiers and sets in this constraint
        """
        node.constraintExpression.setupEnvironment(self)

        if node.indexingExpression:
            node.indexingExpression.setupEnvironment(self)

    def setupEnvironment_ConstraintExpression2(self, node):
        """
        Generate the AMPL code for the identifiers and sets in this constraint
        """
        node.linearExpression1.setupEnvironment(self)
        node.linearExpression2.setupEnvironment(self)

    def setupEnvironment_ConstraintExpression3(self, node):
        """
        Generate the AMPL code for the identifiers and sets in this constraint
        """
        node.numericExpression1.setupEnvironment(self)
        node.linearExpression.setupEnvironment(self)
        node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_ConditionalConstraintExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this constraint expression
        """
        node.logicalExpression.setupEnvironment(self)

        previousLevel = self.level
        previousTable = self.currentTable

        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.constraintExpression1.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable

        if node.constraintExpression2 != None:
            previousLevel = self.level
            previousTable = self.currentTable

            self.level += 1
            self.currentTable.setIsLeaf(False)
            self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

            node.constraintExpression2.setupEnvironment(self)

            self.level = previousLevel
            self.currentTable = previousTable


    # Linear Expression
    def setupEnvironment_ValuedLinearExpression(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this linear expression
        """
        node.value.setupEnvironment(self)

    def setupEnvironment_LinearExpressionBetweenParenthesis(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this linear expression
        """
        previousLevel = self.level
        previousTable = self.currentTable

        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.linearExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable

    def setupEnvironment_LinearExpressionWithArithmeticOperation(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this linear expression
        """
        node.expression1.setupEnvironment(self)
        node.expression2.setupEnvironment(self)

    def setupEnvironment_MinusLinearExpression(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this linear expression
        """
        node.linearExpression.setupEnvironment(self)

    def setupEnvironment_IteratedLinearExpression(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets in this linear expression
        """
        previousLevel = self.level
        previousTable = self.currentTable

        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        if node.numericExpression:
            node.indexingExpression.setHasSup(True)
            node.indexingExpression.setSupExpression(node.numericExpression)
        
        node.indexingExpression.setupEnvironment(self)

        if node.numericExpression:
            node.numericExpression.setupEnvironment(self)

        node.linearExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable
        

    def setupEnvironment_ConditionalLinearExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this linear expression
        """
        node.logicalExpression.setupEnvironment(self)

        if node.linearExpression1 != None:
            previousLevel = self.level
            previousTable = self.currentTable

            self.level += 1
            self.currentTable.setIsLeaf(False)
            self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

            node.linearExpression1.setupEnvironment(self)

            self.level = previousLevel
            self.currentTable = previousTable

        if node.linearExpression2 != None:
            previousLevel = self.level
            previousTable = self.currentTable

            self.level += 1
            self.currentTable.setIsLeaf(False)
            self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

            node.linearExpression2.setupEnvironment(self)

            self.level = previousLevel
            self.currentTable = previousTable

    # Numeric Expression
    def setupEnvironment_NumericExpressionWithFunction(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        if node.numericExpression1 != None:
            node.numericExpression1.setupEnvironment(self)

        if node.numericExpression2 != None:
            node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_FractionalNumericExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        node.numerator.setupEnvironment(self)
        node.denominator.setupEnvironment(self)

    def setupEnvironment_ValuedNumericExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        node.value.setupEnvironment(self)

    def setupEnvironment_NumericExpressionBetweenParenthesis(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        previousLevel = self.level
        previousTable = self.currentTable

        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.numericExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable


    def setupEnvironment_NumericExpressionWithArithmeticOperation(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        node.numericExpression1.setupEnvironment(self)
        node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_MinusNumericExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_IteratedNumericExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        previousLevel = self.level
        previousTable = self.currentTable

        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        if node.supNumericExpression:
            node.indexingExpression.setHasSup(True)
            node.indexingExpression.setSupExpression(node.supNumericExpression)

        node.indexingExpression.setupEnvironment(self)
        
        if node.supNumericExpression:
            node.supNumericExpression.setupEnvironment(self)

        node.numericExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable


    def setupEnvironment_ConditionalNumericExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        node.logicalExpression.setupEnvironment(self)

        previousLevel = self.level
        previousTable = self.currentTable
        
        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.numericExpression1.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable


        if node.numericExpression2 != None:
            previousLevel = self.level
            previousTable = self.currentTable
            
            self.level += 1
            self.currentTable.setIsLeaf(False)
            self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

            node.numericExpression2.setupEnvironment(self)

            self.level = previousLevel
            self.currentTable = previousTable


    # Symbolic Expression
    def setupEnvironment_SymbolicExpressionWithFunction(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        if node.firstExpression != None:
            node.firstExpression.setupEnvironment(self)
            
        if node.numericExpression1 != None:
            node.numericExpression1.setupEnvironment(self)

        if node.numericExpression2 != None:
            node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_StringSymbolicExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        node.value.setupEnvironment(self)

    def setupEnvironment_SymbolicExpressionBetweenParenthesis(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        previousLevel = self.level
        previousTable = self.currentTable

        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.symbolicExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable


    def setupEnvironment_SymbolicExpressionWithOperation(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        node.symbolicExpression1.setupEnvironment(self)
        node.symbolicExpression2.setupEnvironment(self)

    def setupEnvironment_ConditionalSymbolicExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this symbolic expression
        """
        node.logicalExpression.setupEnvironment(self)

        previousLevel = self.level
        previousTable = self.currentTable
        
        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.symbolicExpression1.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable

        if node.symbolicExpression2 != None:
            previousLevel = self.level
            previousTable = self.currentTable
            
            self.level += 1
            self.currentTable.setIsLeaf(False)
            self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

            node.symbolicExpression2.setupEnvironment(self)

            self.level = previousLevel
            self.currentTable = previousTable

    # Indexing Expression
    def setupEnvironment_IndexingExpression(self, node):
        """
        Generate the AMPL code for entries in this indexing expression
        """

        if node.hasSup:
            if len(node.entriesIndexingExpression) != 1 or not isinstance(node.entriesIndexingExpression[0], EntryIndexingExpressionEq):
                raise CodeGenerationException(self.stmtIndex+1, ", ".join(map(lambda el: el.getSymbolName(self.codeGenerator), node.entriesIndexingExpression)), 'Iterated expression (\sum, \prod, \max, \min, \cup or \cap) with a upper limit expression must have a single entry of the form "identifier = identifier2 | numeric expression" as the lower limit expression Ex.: \sum_{i = 1}^{n}x_{i}')
            else:
                node.entriesIndexingExpression[0].setHasSup(True)
                node.entriesIndexingExpression[0].setSupExpression(node.supExpression)

        map(self._setupEntry, node.entriesIndexingExpression)

        if node.logicalExpression:
            node.logicalExpression.setupEnvironment(self)

    def setupEnvironment_EntryExpressionWithSet(self, node, identifier):

        var = None
        if isinstance(identifier, ValueList):
            var = []
            for var1 in identifier.getValues():
                var2 = self._getIdentifier(var1)
                var.append(var2)
        else:
            var = self._getIdentifier(identifier)

        setExpressionObj = self._getSetExpressionObj(node.setExpression)
        setExpression = self._getSetExpression(node.setExpression)

        if isinstance(setExpressionObj, BinarySet):

            if isinstance(var, list):
                for i in range(len(var)):
                    var[i].isBinary = True
            else:
                var.isBinary = True

            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, IntegerSet):
            if isinstance(var, list):
                for i in range(len(var)):
                    var[i].isInteger = True
            else:
                var.isInteger = True

            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, RealSet):
            if isinstance(var, list):
                for i in range(len(var)):
                    var[i].isReal = True
                    var[i].isDeclaredAsVar = True
            else:
                var.isReal = True
                var.isDeclaredAsVar = True

            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, SymbolicSet):
            if isinstance(var, list):
                for i in range(len(var)):
                    var[i].isSymbolic = True
                    self._setIsParam(var[i])
            else:
                self._setIsParam(var)
                var.isSymbolic = True

            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, LogicalSet):
            if isinstance(var, list):
                for i in range(len(var)):
                    var[i].isLogical = True
                    self._setIsParam(var[i])
            else:
                var.isLogical = True
                self._setIsParam(var)

            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, ParameterSet):
            if isinstance(var, list):
                for i in range(len(var)):
                    self._setIsParam(var[i])
                    var[i].isDeclaredAsParam = True
            else:
                self._setIsParam(var)
                var.isDeclaredAsParam = True

            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, VariableSet):
            if isinstance(var, list):
                for i in range(len(var)):
                    self._setIsVar(var[i])
                    var[i].isDeclaredAsVar = True
            else:
                self._setIsVar(var)
                var.isDeclaredAsVar = True

            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, SetSet):
            if isinstance(var, list):
                for i in range(len(var)):
                    self._setIsSet(var[i])
                    var[i].isDeclaredAsSet = True
            else:
                self._setIsSet(var)
                var.isDeclaredAsSet = True

            self._addType(identifier, setExpressionObj)

        if isinstance(var, list):
            for i in range(len(var)):
                var[i].setupEnvironment(self)
        else:
            var.setupEnvironment(self)

    # Entry Indexing Expression
    def setupEnvironment_EntryIndexingExpressionWithSet(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets used in this entry for indexing expression
        """

        if isinstance(node.identifier, str):
            return

        setExpressionObj = self._getSetExpressionObj(node.setExpression)
        setExpression = self._getSetExpression(node.setExpression)

        if isinstance(node.identifier, Tuple):
            tupleVal = node.identifier.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                self._setDimension(node.setExpression, dimen)

        if not self._checkIsModifierSet(setExpressionObj):
            if isinstance(node.identifier, ValueList):
                for var in node.identifier.getValues():
                    var = self._getIdentifier(var)

                    self._addBelongsTo(var, node.setExpression, node.op)
            else:
                var = self._getIdentifier(node.identifier)
                self._addBelongsTo(var, node.setExpression, node.op)

        else:
            if isinstance(node.identifier, ValueList):
                for var in node.identifier.getValues():
                    var = self._getIdentifier(var)

                    self._addDomainExpression(var, node.setExpression, node.op)
            else:
                var = self._getIdentifier(node.identifier)
                self._addBelongsTo(var, node.setExpression, node.op)

        if isinstance(node.identifier, Tuple):
            for var in tupleVal:
                #self.setupEnvironment_EntryExpressionWithSet(node, var)
                var.setupEnvironment(self)

        else:
            self.setupEnvironment_EntryExpressionWithSet(node, node.identifier)

        node.setExpression.setupEnvironment(self)

    def setupEnvironment_EntryIndexingExpressionCmp(self, node):
        """
        Generate the AMPL code for declaration of identifiers and sets used in this entry for indexing expressions
        """
        node.numericExpression.setupEnvironment(self)

    def setupEnvironment_EntryIndexingExpressionEq(self, node):
        """
        Generate the AMPL code for declaration of identifiers and sets used in this entry for indexing expressions
        """
        self._addBelongsTo(node.identifier, node.value, DeclarationAttribute.IN, node.supExpression if node.hasSup else None)

        node.identifier.setupEnvironment(self)
        node.value.setupEnvironment(self)

    def setupEnvironment_LogicalExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this numeric expression
        """
        map(self._setupEntryByKey, node.entriesLogicalExpression)

    # Entry Logical Expression
    def setupEnvironment_EntryLogicalExpressionNot(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets used in this entry for logical expression
        """
        node.logicalExpression.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionNumericOrSymbolic(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets used in this entry for logical expression
        """
        node.numericOrSymbolicExpression.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionRelational(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets used in this entry for logical expression
        """
        node.numericExpression1.setupEnvironment(self)
        node.numericExpression2.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionWithSet(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets used in this entry for logical expression
        """

        if isinstance(node.identifier, str):
            return

        setExpressionObj = self._getSetExpressionObj(node.setExpression)
        setExpression = self._getSetExpression(node.setExpression)

        if isinstance(node.identifier, Tuple):
            tupleVal = node.identifier.getValues()
            dimen = len(tupleVal)

            if dimen > 1:
                self._setDimension(node.setExpression, dimen)

        if not self._checkIsModifierSet(setExpressionObj):
            if isinstance(node.identifier, ValueList):
                for var in node.identifier.getValues():
                    var = self._getIdentifier(var)

                    self._addBelongsTo(var, node.setExpression, node.op)
            else:
                var = self._getIdentifier(node.identifier)
                self._addBelongsTo(var, node.setExpression, node.op)

        else:
            if isinstance(node.identifier, ValueList):
                for var in node.identifier.getValues():
                    var = self._getIdentifier(var)

                    self._addDomainExpression(var, node.setExpression, node.op)
            else:
                var = self._getIdentifier(node.identifier)
                self._addDomainExpression(var, node.setExpression, node.op)

        if isinstance(node.identifier, Tuple):
            for var in tupleVal:
                var.setupEnvironment(self)
        else:
            self.setupEnvironment_EntryExpressionWithSet(node, node.identifier)
        
        node.setExpression.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionWithSetOperation(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets used in this entry for logical expression
        """
        node.setExpression1.setupEnvironment(self)
        node.setExpression2.setupEnvironment(self)

    def setupEnvironment_EntryLogicalExpressionIterated(self, node):
        """
        Generate the AMPL code for the declaration of identifiers and sets used in this entry for logical expression
        """
        previousLevel = self.level
        previousTable = self.currentTable

        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.indexingExpression.setupEnvironment(self)
        node.logicalExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable


    def setupEnvironment_EntryLogicalExpressionBetweenParenthesis(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this logical expression
        """
        previousLevel = self.level
        previousTable = self.currentTable
        
        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.logicalExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable

    # Set Expression
    def setupEnvironment_SetExpressionWithValue(self, node):
        """
        Generate the AMPL code for declaration of identifiers and sets used in this set expression
        """
        if not isinstance(node.value, str):
            if isinstance(node.value, ValueList):
                for var in node.value.getValues():
                    var = self._getIdentifier(var)

                    if isinstance(var, Identifier) and not self.isParamForSure(var):
                        self._setIsSet(var)

                    var.setupEnvironment(self)

            else:
                if isinstance(node.value, Identifier) and not self.isParamForSure(node.value):
                    self._setIsSet(node.value)

                node.value.setupEnvironment(self)

    def setupEnvironment_SetExpressionWithIndices(self, node):
        """
        Generate the AMPL code for declaration of identifiers and sets used in this set expression
        """
        if not isinstance(node.identifier, str):
            if isinstance(node.identifier, Identifier) and not self.isParamForSure(node.identifier):
                self._setIsSet(node.identifier)

            if len(node.indices) > 0:
                if isinstance(node.indices, ValueList):
                    node.identifier.setSubIndices(node.indices.getValues())
                else:
                    var = self._getIdentifier(node.indices)
                    node.identifier.setSubIndices([var])

            node.identifier.setupEnvironment(self)

        if len(node.indices) > 0:
            node.indices.setupEnvironment(self)

    def setupEnvironment_SetExpressionWithOperation(self, node):
        """
        Generate the AMPL code for declaration of identifiers and sets used in this set expression
        """
        node.setExpression1.setupEnvironment(self)
        node.setExpression2.setupEnvironment(self)

    def setupEnvironment_SetExpressionBetweenParenthesis(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this set expression
        """
        previousLevel = self.level
        previousTable = self.currentTable
        
        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.setExpression.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable


    def setupEnvironment_SetExpressionBetweenBraces(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this set expression
        """
        if node.setExpression != None:
            node.setExpression.setupEnvironment(self)

    def setupEnvironment_IteratedSetExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this set expression
        """
        previousLevel = self.level
        previousTable = self.currentTable
        
        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        if node.supExpression != None:
            node.indexingExpression.setHasSup(True)
            node.indexingExpression.setSupExpression(node.supExpression)

        node.indexingExpression.setupEnvironment(self)

        if node.supExpression != None:
            node.supExpression.setupEnvironment(self)

        node.integrand.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable

    def setupEnvironment_ConditionalSetExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets used in this set expression
        """
        node.logicalExpression.setupEnvironment(self)

        previousLevel = self.level
        previousTable = self.currentTable
        
        self.level += 1
        self.currentTable.setIsLeaf(False)
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

        node.setExpression1.setupEnvironment(self)

        self.level = previousLevel
        self.currentTable = previousTable

        if node.setExpression2 != None:
            previousLevel = self.level
            previousTable = self.currentTable
            
            self.level += 1
            self.currentTable.setIsLeaf(False)
            self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex, self.currentTable, True), self.level)

            node.setExpression2.setupEnvironment(self)

            self.level = previousLevel
            self.currentTable = previousTable

    # Range
    def setupEnvironment_Range(self, node):
        """
        Generate the AMPL code for the declaration of identifiers used in this range expression
        """
        if not isinstance(node.rangeInit, str):
            ident = self._getIdentifier(node.rangeInit)

            if isinstance(ident, Identifier):
                self._setIsParam(ident)
                ident.isInt = True

            node.rangeInit.setupEnvironment(self)
        
        if not isinstance(node.rangeEnd, str):
            ident = self._getIdentifier(node.rangeEnd)

            if isinstance(ident, Identifier):
                self._setIsParam(ident)
                ident.isInt = True

            node.rangeEnd.setupEnvironment(self)

        if node.by != None:
            ident = self._getIdentifier(node.by)

            if isinstance(ident, Identifier):
                self._setIsParam(ident)
                ident.isInt = True

            node.by.setupEnvironment(self)
    
    # Value List
    def setupEnvironment_ValueList(self, node):
        """
        Generate the AMPL code for the declaration of identifiers used in this range expression
        """
        map(self._setupValue, node.values)

    # Identifier List
    def setupEnvironment_IdentifierList(self, node):
        """
        Generate the AMPL code for the declaration of identifiers used in this range expression
        """
        map(self._setupValue, node.identifiers)

    # Tuple
    def setupEnvironment_Tuple(self, node):
        """
        Generate the AMPL code for the declaration of identifiers used in this range expression
        """
        map(self._setupValue, node.values)

    # Tuple List
    def setupEnvironment_TupleList(self, node):
        """
        Generate the AMPL code for the declaration of identifiers used in this range expression
        """
        map(self._setupValue, node.values)

    # Value
    def setupEnvironment_Value(self, node):
        """
        Generate the AMPL code for the declaration of the identifier of this value
        """
        node.value.setupEnvironment(self)

    # Identifier
    def setupEnvironment_Identifier(self, node):
        """
        Generate the AMPL code for the declaration of this identifier
        """

        if node.getIndice() > -1:
            node.isInt = True
            if len(node.sub_indices) == 0:
                return
        
        self.identifier = node
        self.identifierKey = node.getSymbolName(self.codeGenerator)
        
        _symbolTableEntry = self.currentTable.lookup(self.identifierKey)
        if _symbolTableEntry == None:
            justInserted = True
            _symbolTableEntry = SymbolTableEntry(self.identifierKey, node, GenProperties(self.identifierKey), None, self.level, 
                                                 [map(lambda el: el.getSymbolName(self.codeGenerator), node.sub_indices)] if node.sub_indices != None else [])
            self.currentTable.insert(self.identifierKey, _symbolTableEntry)
            
        elif node.sub_indices != None:
            _symbolTableEntry.addSubIndices(map(lambda el: el.getSymbolName(self.codeGenerator), node.sub_indices))

        if (node.isVar or node.isDeclaredAsVar or self.codeGenerator.genVariables.has(self.identifierKey)) and not self.isDeclaredAsParam(node) and not self.isDeclaredAsSet(node):

            _genVar = self.codeGenerator.genVariables.get(self.identifierKey)
            if node.isDeclaredAsVar and _genVar != None:
                _genVar.setCertainty(True)
                _genVar.setIsDeclaredAsVar(True)

            elif node.isDeclaredAsVar or (not _genVar and not self.isDeclaredAsSet(node) and not self.isDeclaredAsParam(node)): # check if this identifier was not seen yet

                self.codeGenerator.genParameters.remove(self.identifierKey)
                self.codeGenerator.genSets.remove(self.identifierKey)

                _genVar = GenVariable(self.identifierKey, None)
                if (node.isVar != None and not node.isVar) or (node.isDeclaredAsVar != None and not node.isDeclaredAsVar):
                    _genVar.setCertainty(False)

                if node.isDeclaredAsVar:
                    _genVar.setCertainty(True)
                    _genVar.setIsDeclaredAsVar(True)

                _symbolTableEntry = self.currentTable.lookup(self.identifierKey)
                if _symbolTableEntry.getInferred() or node.isDeclaredAsVar:
                    _symbolTableEntry.setType(Constants.VARIABLES)

                if node.isDeclaredAsVar:
                    _symbolTableEntry.setInferred(False)
                
                self.codeGenerator.genVariables.add(_genVar)

            self._checkSubIndices(node)

        elif (node.isSet or node.isDeclaredAsSet) and not self.isDeclaredAsParam(node) and not self.isDeclaredAsVar(node):
            _genSet = self.codeGenerator.genSets.get(self.identifierKey)
            if node.isDeclaredAsSet and _genSet != None:
                _genSet.setCertainty(True)
                _genSet.setIsDeclaredAsSet(True)
            
            elif node.isDeclaredAsSet or (not _genSet and not self.isDeclaredAsVar(node) and not self.isDeclaredAsParam(node)): # check if this identifier was not seen yet

                self.codeGenerator.genParameters.remove(self.identifierKey)
                self.codeGenerator.genVariables.remove(self.identifierKey)

                _genSet = GenSet(self.identifierKey, node.dimenSet)
                if (node.isSet != None and not node.isSet) or (node.isDeclaredAsSet != None and not node.isDeclaredAsSet):
                    _genSet.setCertainty(False)

                if node.isDeclaredAsSet:
                    _genSet.setCertainty(True)
                    _genSet.setIsDeclaredAsSet(True)

                if _symbolTableEntry.getInferred() or node.isDeclaredAsSet:
                    _symbolTableEntry.setType(Constants.SETS)

                if node.isDeclaredAsSet:
                    _symbolTableEntry.setInferred(False)

                self.codeGenerator.genSets.add(_genSet)

            self._checkSubIndices(node)

        elif (node.isDeclaredAsParam or (not node.isInSet and not self.codeGenerator.genBelongsToList.has(GenBelongsTo(self.identifierKey, self.stmtIndex)))) and not self.isDeclaredAsVar(node) and not self.isDeclaredAsSet(node):
            _genParam = self.codeGenerator.genParameters.get(self.identifierKey)
            if node.isDeclaredAsParam and _genParam != None:
                _genParam.setCertainty(True)
                _genParam.setIsDeclaredAsParam(True)
            
            elif node.isDeclaredAsParam or (not _genParam and not self.isDeclaredAsVar(node) and not self.isDeclaredAsSet(node)): # check if this param was not seen yet

                self.codeGenerator.genSets.remove(self.identifierKey)
                self.codeGenerator.genVariables.remove(self.identifierKey)

                _genParam = GenParameter(self.identifierKey, node.isSymbolic or node.isLogical, node.isInt or node.isInteger, str(self.stmtIndex))
                if (node.isParam != None and not node.isParam) or (node.isDeclaredAsParam != None and not node.isDeclaredAsParam):
                    _genParam.setCertainty(False)

                if node.isDeclaredAsParam:
                    _genParam.setCertainty(True)
                    _genParam.setIsDeclaredAsParam(True)

                if _symbolTableEntry.getInferred() or node.isDeclaredAsParam:
                    _symbolTableEntry.setType(Constants.PARAMETERS)

                if node.isDeclaredAsParam:
                    _symbolTableEntry.setInferred(False)

                self.codeGenerator.genParameters.add(_genParam)

            elif node.isSymbolic or node.isLogical or node.isInt or node.isInteger:
                _genParam = self.codeGenerator.genParameters.get(self.identifierKey)
                if _genParam != None:
                    if node.isSymbolic or node.isLogical:
                        _genParam.setIsSymbolic(True)

                    if node.isInt or node.isInteger:
                        _genParam.setIsInteger(True)

            self._checkSubIndices(node)

        else:
            self._checkSubIndices(node)

        self.identifier = None
        self.identifierKey = None

    def setupEnvironment_Number(self, node):

        if node.getIndice() == -1:
            return

        num = int(node.getSymbolName(self.codeGenerator))

        _symbolTableEntry = self.currentTable.lookup(node.getIdentifierName())
        if _symbolTableEntry == None:
            _symbolTableEntry = SymbolTableEntry(self.identifierKey, self.identifier, GenProperties(self.identifierKey, [], None, 
                                                {node.getIndice(), num}, {node.getIndice(), num}), None, self.level, [])
            self.currentTable.insert(self.identifierKey, _symbolTableEntry)

        else:
            _symbolTableEntry.getProperties().setMinValByIndex(node.getIndice(), num)
            _symbolTableEntry.getProperties().setMaxValByIndex(node.getIndice(), num)

    def setupEnvironment_ID(self, node):
        pass

    def setupEnvironment_IntegerSet(self, node):
        pass

    def setupEnvironment_RealSet(self, node):
        pass

    def setupEnvironment_BinarySet(self, node):
        pass

    def setupEnvironment_LogicalSet(self, node):
        pass

    def setupEnvironment_SymbolicSet(self, node):
        pass

    def setupEnvironment_ParameterSet(self, node):
        pass

    def setupEnvironment_SetSet(self, node):
        pass

    def setupEnvironment_VariableSet(self, node):
        pass

    def setupEnvironment_String(self, node):
        pass

    def setupEnvironment_Infinity(self, node):
        pass

    # Declarations
    def setupEnvironment_Declarations(self, node):
        map(self._setupDeclaration, node.declarations)
    
    def setupEnvironment_Declaration(self, node):
        """
        Generate the AMPL code for declaration of identifiers and sets in this declaeation
        """
        self.currentTable = self.codeGenerator.symbolTables.insert(self.stmtIndex, SymbolTable(self.stmtIndex), 0, True)

        for identifier in node.declarationExpression.identifiers:
            identifier = self._getIdentifier(identifier)
            
            if isinstance(identifier, Identifier):
                name = identifier.getSymbolName(self.codeGenerator)
                genDeclaration = self.codeGenerator.genDeclarations.get(name)

                if genDeclaration == None:
                    _sub_indices = {}
                    if identifier.sub_indices:
                        _sub_indices = {self.stmtIndex: identifier.sub_indices}

                    genDeclaration = GenDeclaration(name, list(node.declarationExpression.attributeList), None, _sub_indices, self.stmtIndex)
                    self.codeGenerator.genDeclarations.add(genDeclaration)

                else:
                    genDeclaration.addAttributes(node.declarationExpression.attributeList)

                    if identifier.sub_indices:
                        genDeclaration.addSubIndices({self.stmtIndex: identifier.sub_indices})
                    
                if node.indexingExpression:
                    genDeclaration.addIndexingExpression({self.stmtIndex: node.indexingExpression})

                _symbolTableEntry = self.currentTable.lookup(name)
                if _symbolTableEntry == None:
                    _symbolTableEntry = SymbolTableEntry(name, identifier, GenProperties(name, [], None, None, None, None, genDeclaration), 
                                                         None, self.level, [], True, True)
                    self.currentTable.insert(name, _symbolTableEntry)
                    
                else:
                    _symbolTableEntry.getProperties().setAttributes(genDeclaration)

        node.declarationExpression.setupEnvironment(self)

        if node.indexingExpression:
            node.indexingExpression.setupEnvironment(self)

    def setupEnvironment_DeclarationExpression(self, node):
        """
        Generate the AMPL code for the identifiers and sets in this declaration
        """

        for identifier in node.identifiers:
            identifier = self._getIdentifier(identifier)
            
            if isinstance(identifier, Identifier):
                
                identifier.setIsParam(False)
                name = identifier.getSymbolName(self.codeGenerator)
                
                if self.codeGenerator.genSets.has(name):
                    self._setIsSet(identifier)

                map(lambda el: self.setupEnvironment_AttributeListPre(el, identifier), node.attributeList)
                map(lambda el: self.setupEnvironment_AttributeList(el, identifier), node.attributeList)

        for identifier in node.identifiers:
            identifier = self._getIdentifier(identifier)
            identifier.setupEnvironment(self)

        map(lambda el: el.setupEnvironment(self), node.attributeList)

    def setupEnvironment_DeclarationAttribute(self, node):
        """
        Generate the AMPL code for the identifiers and sets in this declaration
        """
        node.attribute.setupEnvironment(self)

    def setupEnvironment_AttributeListPre(self, node, identifier):
        var = self._getIdentifier(node.attribute)

        if isinstance(var, str):
            name = var
        else:
            name = var.getSymbolName(self.codeGenerator)

        if node.op == DeclarationAttribute.IN:
            self.setupEnvironment_DeclarationExpressionWithSet(node.attribute, identifier)

        elif (node.op == DeclarationAttribute.ST or node.op == DeclarationAttribute.DF or node.op == DeclarationAttribute.WT) and \
            (isinstance(node.attribute, SetExpression) or isinstance(var, SetExpression) or isinstance(var, Range) or self.codeGenerator.genSets.has(name)) and not identifier.isParam:

            if not self.codeGenerator.genParameters.has(name):
                self._setIsSet(identifier)
                
                if isinstance(var, Identifier):
                    self._setIsSet(var)

    def setupEnvironment_AttributeList(self, node, identifier):
        identifier1 = self._getIdentifier(node.attribute)
        if (node.op == DeclarationAttribute.ST or node.op == DeclarationAttribute.DF) and identifier.isParam and isinstance(identifier1, Identifier):

            name = identifier1.getSymbolName(self.codeGenerator)
            param = self.codeGenerator.genParameters.get(name)
            if param != None:
                param.setCertainty(True)

            self._setIsParam(identifier1)
            self._setIsParam(identifier)
        
    def setupEnvironment_DeclarationExpressionWithSet(self, attribute, identifier):
        name = identifier.getSymbolName(self.codeGenerator)
        setExpressionObj = self._getSetExpressionObj(attribute)
        setExpression = self._getSetExpression(attribute)

        _symbolTableEntry = self.currentTable.lookup(name)
        if _symbolTableEntry == None:
            _symbolTableEntry = SymbolTableEntry(name, identifier, GenProperties(name, 
                                                 [GenItemDomain(setExpression, DeclarationAttribute.IN, attribute.getDependencies(self.codeGenerator), 
                                                 setExpressionObj)], None, None, None), None, self.level, [], True, True)
            self.currentTable.insert(name, _symbolTableEntry)

        else:
            if _symbolTableEntry.getInferred():
                _symbolTableEntry.setType(None)

            _symbolTableEntry.getProperties().addDomain(GenItemDomain(setExpression, DeclarationAttribute.IN, 
                                                        attribute.getDependencies(self.codeGenerator), setExpressionObj))

        if isinstance(setExpressionObj, BinarySet):
            identifier.isBinary = True
            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, IntegerSet):
            identifier.isInteger = True
            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, RealSet):
            identifier.isReal = True
            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, SymbolicSet):
            self._setIsParam(identifier)
            identifier.isSymbolic = True
            self._addType(identifier, setExpressionObj)
            
        elif isinstance(setExpressionObj, LogicalSet):
            self._setIsParam(identifier)
            identifier.isLogical = True
            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, ParameterSet):
            self._setIsParam(identifier)
            identifier.isDeclaredAsParam = True
            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, VariableSet):
            self._setIsVar(identifier)
            identifier.isDeclaredAsVar = True
            self._addType(identifier, setExpressionObj)

        elif isinstance(setExpressionObj, SetSet):
            self._setIsSet(identifier)
            identifier.isDeclaredAsSet = True
            self._addType(identifier, setExpressionObj)
