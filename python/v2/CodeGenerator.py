from Utils import *
from ValueList import *
from EntryIndexingExpression import *
from TopologicalSort import *
from GenSets import *
from GenVariables import *
from GenParameters import *
from GenDomains import *
from GenTypes import *
from GenTuples import *
from GenSet import *
from GenVariable import *
from GenParameter import *
from GenDomain import *
from GenType import *
from GenTuple import *

class CodeGenerator:
    """ Visitor in the Visitor Pattern """
    
    def __init__(self):
        self.genSets = GenSets()
        self.genVariables = GenVariables()
        self.genParameters = GenParameters()
        self.genDomains = GenDomains()
        self.genTypes = GenTypes()
        self.genTuples = GenTuples()
        self.topological_order = []

        self.constraintNumber = 0;

    def generateCode(self, node):
        cls = node.__class__
        method_name = 'generateCode_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    def _generateGraphAux(self, graph, genObj, genObjOther):
        if len(genObj) > 0:
            for paramIn in genObj.getAll():
                if not paramIn.getName() in graph:
                    graph[paramIn.getName()] = []

                if len(paramIn.getSubIndices()) > 0:
                    
                    _subIndices = paramIn.getSubIndices().getAll()
                    _tuple = self._getTuple(_subIndices)

                    if _tuple != None:
                        graph[paramIn.getName()].append(_tuple.getName())
                        continue

                    for paramDomain in _subIndices:
                        _var = self.genDomains.get(paramDomain.getName())

                        if _var != None:
                            _domain = _var.getDomain()
                            if _domain != None:
                                if ".." in _domain:
                                    param = _domain.split("..")

                                    if param and param[1] and (genObj.has(param[1]) or genObjOther.has(param[1])):
                                        graph[paramIn.getName()].append(param[1])

                                else:
                                    param = _domain.split("[")

                                    if param and param[0] and (genObj.has(param[0]) or genObjOther.has(param[0])):
                                        graph[paramIn.getName()].append(param[0])

    # Auxiliary Methods
    def _generateGraph(self):
        graph = {}

        self._generateGraphAux(graph, self.genParameters, self.genSets)
        self._generateGraphAux(graph, self.genSets, self.genParameters)

        return graph

    # Get the MathProg code for a given relational expression
    def _getCodeValue(self, value):
        val = value.generateCode(self)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given sub-indice
    def _getCodeID(self, id_):
        val = id_.generateCode(self)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given constraint
    def _getCodeConstraint(self, constraint):
        self.constraintNumber += 1
        return "s.t. C" + str(self.constraintNumber) + " " + constraint.generateCode(self)

    # Get the MathProg code for a given entry
    def _getCodeEntry(self, entry): return entry.generateCode(self)

    # Get the MathProg code for a given entry
    def _getCodeEntryByKey(self, entry):
        for key in entry:
            return key, entry[key].generateCode(self)

    def _getDomain(self, var):
        _domain = self.genDomains.get(var.getName())
        if _domain != None and _domain.getDomain() != None:
            if ".." in _domain.getDomain():
                return _domain.getDomain()
            else:
                return var.getName() + " in " + _domain.getDomain()

        elif var.getMinVal() < float('inf'):
            res = ""
            if isinstance(var.getParent().getParent(), GenSet):
                res += var.getName() + " in "
            
            res += str(var.getMinVal()) + ".." + str(var.getMaxVal())
            return res

        else:
            return ""

    def _declareVars(self):
        """
        Generate the MathProg code for the declaration of variables
        """
        if len(self.genVariables) > 0:
            varStr = ""
            for var in self.genVariables.getAll():
                if not self.genParameters.has(var) and not self.genSets.has(var):

                    if len(var.getSubIndices()) == 0:
                        varStr += "var " + var.getName()
                    else:
                        domain = ", ".join(map(self._getDomain, var.getSubIndices().getAll()))
                        if domain:
                            varStr += "var " + var.getName() + "{" + domain + "}"
                        else:
                            varStr += "var " + var.getName()

                    _type = self.genTypes.get(var)
                    if _type != None and _type.getVarType().strip() != "":
                        varStr += " " + _type.getVarType()

                    varStr += ";\n\n"

            return varStr
        else:
            return ""

    def _declareSets(self):
        """
        Generate the MathProg code for the declaration of sets
        """

        if len(self.genSets) > 0:
            setStr = ""
            for setIn in self.genSets.getAll():
                if not self.genParameters.has(setIn):
                    if len(setIn.getSubIndices()) == 0:
                        setStr += "set " + setIn.getName()
                    else:
                        domain = ", ".join(map(self._getDomain, setIn.getSubIndices().getAll()))
                        if domain:
                            setStr += "set " + setIn.getName() + "{" + domain + "}"
                        else:
                            setStr += "set " + setIn.getName()

                    if setIn.getDimension() > 1:
                        dimen = " dimen " + str(setIn.getDimension())
                    else:
                        dimen = ""

                    setStr += dimen + ";\n\n"

            return setStr
        else:
            return ""

    def _getTuple(self, sub_indices):
        """
        Get a tuple with sub-indices
        """
        subIndices = set(map(lambda var: var.getName(), sub_indices))

        for _tuple in self.genTuples.getAll():
            if subIndices == set(_tuple.getTupleVal()):
                return _tuple

        return None

    def _declareParams(self):
        """
        Generate the MathProg code for the declaration of params
        """
        graph = self._generateGraph()
        self.topological_order = sort_topologically_stackless(graph)

        if len(self.genParameters) > 0:
            paramStr = ""

            for paramIn in self.topological_order:
                _genParameter = self.genParameters.get(paramIn)
                
                if len(_genParameter.getSubIndices()) == 0:
                    paramStr += "param " + paramIn
                else:
                    _subIndices = _genParameter.getSubIndices().getAll()
                    _tuple = self._getTuple(_subIndices)

                    if _tuple != None:
                        domain = "("+",".join(_tuple.getTupleVal()) + ") " + _tuple.getOp() + " " + _tuple.getName()
                    else:
                        domain = ", ".join(map(self._getDomain, _subIndices))

                    if domain:
                        paramStr += "param " + paramIn + "{" + domain + "}"
                    else:
                        paramStr += "param " + paramIn

                _type = self.genTypes.get(paramIn)
                if _type != None:
                    paramStr += " " + _type.getVarType()

                paramStr += ";\n\n"

            return paramStr
        else:
            return ""

    def _declareParam(self, _genParameter):
        paramStr = ""
        paramIn = _genParameter.getName()

        if len(_genParameter.getSubIndices()) == 0:
            paramStr += "param " + paramIn

        else:
            _subIndices = _genParameter.getSubIndices().getAll()
            _tuple = self._getTuple(_subIndices)

            if _tuple != None:
                domain = "("+",".join(_tuple.getTupleVal()) + ") " + _tuple.getOp() + " " + _tuple.getName()
            else:
                domain = ", ".join(map(self._getDomain, _subIndices))

            if domain:
                paramStr += "param " + paramIn + "{" + domain + "}"
            else:
                paramStr += "param " + paramIn

        _type = self.genTypes.get(paramIn)
        if _type != None:
            paramStr += " " + _type.getVarType()

        paramStr += ";\n\n"

        return paramStr

    def _declareSet(self, _genSet):
        setStr = ""

        if len(_genSet.getSubIndices()) == 0:
            setStr += "set " + _genSet.getName()
        else:
            domain = ", ".join(map(self._getDomain, _genSet.getSubIndices().getAll()))
            if domain:
                setStr += "set " + _genSet.getName() + "{" + domain + "}"
            else:
                setStr += "set " + _genSet.getName()

        if _genSet.getDimension() > 1:
            dimen = " dimen " + str(_genSet.getDimension())
        else:
            dimen = ""

        setStr += dimen + ";\n\n"

        return setStr

    def _declareSetsAndParams(self):
        graph = self._generateGraph()
        self.topological_order = sort_topologically_stackless(graph)
        paramSetStr = ""

        if len(self.topological_order) > 0:
            for paramSetIn in self.topological_order:
                _genObj = self.genParameters.get(paramSetIn)

                if _genObj != None:
                    paramSetStr += self._declareParam(_genObj)
                else:
                    _genObj = self.genSets.get(paramSetIn)

                    if _genObj != None:
                        paramSetStr += self._declareSet(_genObj)

        return paramSetStr

    def _declareData(self):
        res = "data;\n\n"
        
        if len(self.genSets) > 0:
            for setIn in self.genSets.getAll():
                if not self.genParameters.has(setIn):
                    if len(setIn.getSubIndices()) > 0:
                        dimenIdx = "[" + ",".join(["0"] * len(setIn.getSubIndices())) + "]"
                    else:
                        dimenIdx = ""

                    res += "set " + setIn.getName() + dimenIdx + " :=;\n\n"

        res += "\n"

        if len(self.genParameters) > 0:
            for paramIn in self.topological_order:
                _genParameter = self.genParameters.get(paramIn)
                
                value = ""
                if len(_genParameter.getSubIndices()) == 0:
                    value += " 0"

                res += "param " + paramIn + " :=" + value + ";\n\n"

        res += "\n"

        return res

    def _declareDataParam(self, _genParameter):
        res = ""
        value = ""

        if len(_genParameter.getSubIndices()) == 0:
            value += " 0"

        res += "param " + _genParameter.getName() + " :=" + value + ";\n\n"

        return res

    def _declareDataSet(self, _genSet):
        res = ""

        if len(_genSet.getSubIndices()) > 0:
            dimenIdx = "[" + ",".join(["0"] * len(_genSet.getSubIndices())) + "]"
        else:
            dimenIdx = ""

        res += "set " + _genSet.getName() + dimenIdx + " :=;\n\n"

        return res

    def _declareDataSetsAndParams(self):
        res = "data;\n\n"

        if len(self.topological_order) > 0:
            for paramSetIn in self.topological_order:
                _genObj = self.genParameters.get(paramSetIn)

                if _genObj != None:
                    res += self._declareDataParam(_genObj)
                else:
                    _genObj = self.genSets.get(paramSetIn)

                    if _genObj != None:
                        res += self._declareDataSet(_genObj)

        res += "\n"

        return res

    # Linear Program
    def _preModel(self):
        #return self._declareSets() + "\n" + self._declareParams() + "\n" + self._declareVars() + "\n"
        return self._declareSetsAndParams() + "\n" + self._declareVars() + "\n"

    def _posModel(self):
        res = "\nsolve;\n\n\n"
        #res += self._declareData()
        res += self._declareDataSetsAndParams()
        res += "\nend;\n"

        return res

    def generateCode_LinearProgram(self, node):
        if node.constraints:
            return self._preModel() + "\n" + node.objective.generateCode(self) + "\n\n" + node.constraints.generateCode(self) + "\n\n" + self._posModel() + "\n"
        else:
            return self._preModel() + "\n" + node.objective.generateCode(self) + "\n" + self._posModel() + "\n"

    # Objective Function
    def generateCode_Objective(self, node):
        """
        Generate the code in MathProg for this Objective
        """
        
        if node.domain:
            domain_str = " {" + node.domain.generateCode(self) + "}"
        else:
            domain_str = ""

        return node.type + " obj" + domain_str + ": " + node.linearExpression.generateCode(self) + ";"

    # Constraints
    def generateCode_Constraints(self, node):
        return "\n\n".join(map(self._getCodeConstraint, node.constraints))

    def generateCode_Constraint(self, node):
        res = ""

        if node.indexingExpression:
            # Get the MathProg code for each constraint expression in for clause and concatenates with \n
            res += "{" + node.indexingExpression.generateCode(self) + "} :\n\t"
        else:
            res += " : "

        res += node.constraintExpression.generateCode(self) + ";"

        return res

    def generateCode_ConstraintExpression2(self, node):
        return node.linearExpression1.generateCode(self) + ", " + node.op + " " + node.linearExpression2.generateCode(self)

    def generateCode_ConstraintExpression3(self, node):
        return node.numericExpression1.generateCode(self) + ", " + node.op + " " + node.linearExpression.generateCode(self) + ", " + node.op + " " + node.numericExpression2.generateCode(self)

    # Linear Expression
    def generateCode_ValuedLinearExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_LinearExpressionBetweenParenthesis(self, node):
        return "(" + node.linearExpression.generateCode(self) + ")"

    def generateCode_LinearExpressionWithArithmeticOperation(self, node):
        return node.expression1.generateCode(self) + " " + node.op + " " + node.expression2.generateCode(self)

    def generateCode_MinusLinearExpression(self, node):
        return "-" + node.linearExpression.generateCode(self)

    def generateCode_IteratedLinearExpression(self, node):
        SUM = "sum"

        if node.numericExpression:
            res = SUM + "{" + node.indexingExpression.generateCode(self) + "..(" + node.numericExpression.generateCode(self) + ")}"
        else:
            res = SUM + "{" + node.indexingExpression.generateCode(self) + "}"

        res += "(" + node.linearExpression.generateCode(self) + ")"

        return res

    # Numeric Expression
    def generateCode_NumericExpressionWithFunction(self, node):
        return str(node.function) + "(" + node.numericExpression.generateCode(self) + ")"

    def generateCode_ValuedNumericExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_NumericExpressionBetweenParenthesis(self, node):
        return "(" + node.numericExpression.generateCode(self) + ")"

    def generateCode_NumericExpressionWithArithmeticOperation(self, node):
        return node.numericExpression1.generateCode(self) + " " + node.op + " " + node.numericExpression2.generateCode(self)

    def generateCode_MinusNumericExpression(self, node):
        return "-" + node.numericExpression.generateCode(self)

    def generateCode_IteratedNumericExpression(self, node):
        if node.supNumericExpression:
            res = str(node.op) + "{" + node.indexingExpression.generateCode(self) + "..(" + node.supNumericExpression.generateCode(self) + ")}"
        else:
            res = str(node.op) + "{" + node.indexingExpression.generateCode(self) + "}"

        res += node.numericExpression.generateCode(self)

        return res

    # Indexing Expression
    def generateCode_IndexingExpression(self, node):
        entrySets = []
        for entry in node.entriesIndexingExpression:
            if isinstance(entry, EntryIndexingExpressionWithSet):
                entrySets.append(entry.setExpression.generateCode(self))

        entrySetsTopologicalOrder = [elem for elem in self.topological_order if elem in entrySets]

        entries = node.entriesIndexingExpression
        entriesNew = []

        for entrySet in entrySetsTopologicalOrder:
            entriesToRemove = []
            for entry in entries:
                if isinstance(entry, EntryIndexingExpressionWithSet):
                    if entry.setExpression.generateCode(self) == entrySet:
                        entriesNew.append(entry)
                        entriesToRemove.append(entry)
            
            for entry in entriesToRemove:
                entries.remove(entry)

        for entry in entries:
            entriesNew.append(entry)

        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, entriesNew))
        res = ", ".join(indexing)

        if node.logicalExpression:
            res += " : " + node.logicalExpression.generateCode(self)

        return res
    
    # Entry Indexing Expression
    def generateCode_EntryIndexingExpressionWithSet(self, node):
        if node.isBinary or node.isInteger or node.isNatural or node.isReal or Utils._isInstanceOfStr(node.variable):
            return ""
        elif isinstance(node.variable, ValueList):
            return ", ".join(map(lambda var: var.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self), node.variable.getValues()))
        else:
            return node.variable.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)

    def generateCode_EntryIndexingExpressionCmp(self, node):
        return node.variable.generateCode(self) + " " + node.op + " " + node.numericExpression.generateCode(self)

    def generateCode_EntryIndexingExpressionEq(self, node):
        if node.hasSup:
            return node.variable.generateCode(self) + " in " + Utils._getInt(node.value.generateCode(self))
        else:
            return node.variable.generateCode(self) + " in " + node.value.generateCode(self)

    # Logical Expression
    def generateCode_LogicalExpression(self, node):
        res = ""
        first = True

        for i in range(len(node.entriesLogicalExpression)):
            conj, code = self._getCodeEntryByKey(node.entriesLogicalExpression[i])

            if code != 0:
                if first:
                    first = False
                    res += code
                else:
                    res += " " + conj + " " + code

        return res

    # Entry Logical Expression
    def generateCode_EntryLogicalExpressionRelational(self, node):
        return node.numericExpression1.generateCode(self) + " " + node.op + " " + node.numericExpression2.generateCode(self)

    def generateCode_EntryLogicalExpressionWithSet(self, node):
        if node.isBinary or node.isInteger or node.isNatural or node.isReal:
            return ""
        else:
            return node.value.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionWithSetOperation(self, node):
        return node.setExpression1.generateCode(self) + " " + node.op + " " + node.setExpression2.generateCode(self)

    def generateCode_EntryLogicalExpressionIterated(self, node):
        return node.op + "{" + node.indexingExpression.generateCode(self) + "} " +  node.logicalExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionBetweenParenthesis(self, node):
        return "(" + node.logicalExpression.generateCode(self) + ")"

    # Set Expression
    def generateCode_SetExpressionWithValue(self, node):
        if not Utils._isInstanceOfStr(node.value):
            return node.value.generateCode(self)
        else:
            return node.value

    def generateCode_SetExpressionWithIndices(self, node):
        var_gen = ""
        if not Utils._isInstanceOfStr(node.variable):
            var_gen = node.variable.generateCode(self)
        else:
            var_gen = node.variable

        #return  var_gen + "[" + node.indices.generateCode(self) + "]"
        return  var_gen

    def generateCode_SetExpressionWithOperation(self, node):
        return node.setExpression1.generateCode(self) + " " + node.op + " " + node.setExpression2.generateCode(self)

    # Range
    def generateCode_Range(self, node):
        initValue = node.rangeInit.generateCode(self)
        initValue = Utils._getInt(initValue)

        endValue = node.rangeEnd.generateCode(self)
        endValue = Utils._getInt(endValue)

        return initValue + ".." + endValue

    # Value List
    def generateCode_ValueList(self, node):
        return ",".join(map(self._getCodeValue, node.values))

    # Tuple List
    def generateCode_TupleList(self, node):
        return "(" + ",".join(map(self._getCodeValue, node.values)) + ")"

    # Value
    def generateCode_Value(self, node):
        return node.value.generateCode(self)

    # Variable
    def generateCode_Variable(self, node):
        if Utils._isInstanceOfStr(node.sub_indices):
            return ""

        if len(node.sub_indices) > 0:
            if Utils._isInstanceOfList(node.sub_indices):
                res = node.variable.generateCode(self) + "[" + ",".join(map(self._getCodeID, node.sub_indices)) + "]"
            else:
                res = node.variable.generateCode(self) + "[" + self._getCodeID(node.sub_indices) + "]"
        
        else:
            res = node.variable.generateCode(self)
        
        return res

    # Number
    def generateCode_Number(self, node):
        return str(node.number)

    # ID
    def generateCode_ID(self, node):
        return node.variable
