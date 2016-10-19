from Utils import *
from ValueList import *
from TopologicalSort import *

class CodeGenerator:
    """ Visitor in the Visitor Pattern """
    
    def __init__(self):
        self.Sets = {}
        self.Vars = {}
        self.Params = {}
        self.Indices = {}
        self.Types = {}
        self.Tuples = {}

        self.constraintNumber = 0;
        self.SetsNumber = 0;
        self.VarsNumber = 0;
        self.ParamsNumber = 0;

    def generateCode(self, node):
        cls = node.__class__
        method_name = 'generateCode_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    # Auxiliary Methods

    def _generateGraph(self):
        graph = {}

        if len(self.Params) > 0:
            for paramIn in self.Params:
                if not paramIn in graph:
                    graph[paramIn] = []

                if len(self.Params[paramIn]["sub-indices"]) > 0:

                    for paramDomain in self.Params[paramIn]["sub-indices"]:
                        if paramDomain["var"] in self.Indices:
                            if ".." in self.Indices[paramDomain["var"]]:
                                param = self.Indices[paramDomain["var"]].split("..")

                                if param and param[1] and param[1] in self.Params:
                                    graph[paramIn].append(param[1])
                            else:
                                param = self.Indices[paramDomain["var"]].split("[")

                                if param and param[0] and param[0] in self.Params:
                                    graph[paramIn].append(param[0])

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

    def _getVarDomain(self, varDomain):
        """
        Generate the MathProg code for the declaration of the domain of a variable
        """
        if varDomain["var"] in self.Indices:
            if ".." in self.Indices[varDomain["var"]]:
                return self.Indices[varDomain["var"]]
            else:
                return varDomain["var"] + " in " + self.Indices[varDomain["var"]]
        elif varDomain["min"] < float('inf'):
            return str(varDomain["min"]) + ".." + str(varDomain["max"])
        else:
            return ""

    def _getSetDomain(self, setDomain):
        """
        Generate the MathProg code for the declaration of the domain of a set
        """
        if setDomain["var"] in self.Indices:
            if ".." in self.Indices[setDomain["var"]]:
                return self.Indices[setDomain["var"]]
            else:
                return setDomain["var"] + " in " + self.Indices[setDomain["var"]]
        elif setDomain["min"] < float('inf'):
            return setDomain["var"] + " in " + str(setDomain["min"]) + ".." + str(setDomain["max"])
        else:
            return ""

    def _getParamDomain(self, paramDomain):
        """
        Generate the MathProg code for the declaration of the domain of a parameter
        """
        if paramDomain["var"] in self.Indices:
            if ".." in self.Indices[paramDomain["var"]]:
                return self.Indices[paramDomain["var"]]
            else:
                return paramDomain["var"] + " in " + self.Indices[paramDomain["var"]]
        elif paramDomain["min"] < float('inf'):
            return str(paramDomain["min"]) + ".." + str(paramDomain["max"])
        else:
            return ""
        
    def _declareVars(self):
        """
        Generate the MathProg code for the declaration of variables
        """
        if len(self.Vars) > 0:

            varStr = ""
            for var in self.Vars:
                if not var in self.Params and not var in self.Sets:
                    if len(self.Vars[var]["sub-indices"]) == 0:
                        varStr += "var " + var
                    else:
                        domain = ", ".join(map(self._getVarDomain, self.Vars[var]["sub-indices"]))
                        if domain:
                            varStr += "var " + var + "{" + domain + "}"
                        else:
                            varStr += "var " + var

                    if var in self.Types and self.Types[var]:
                        varStr += " " + self.Types[var]

                    varStr += ";\n"

            return varStr
        else:
            return ""

    def _declareSets(self):
        """
        Generate the MathProg code for the declaration of sets
        """
        if len(self.Sets) > 0:
            setStr = ""
            for setIn in self.Sets:

                if not setIn in self.Params:
                    setStr += "set " + setIn + ";\n"

            return setStr
        else:
            return ""

    def _getTuple(self, sub_indices):
        """
        Get a tuple with sub-indices
        """
        subIndices = set(map(lambda var: var["var"], sub_indices))

        for key in self.Tuples:
            if subIndices == set(self.Tuples[key]["tuple"]):
                return key

        return None

    def _declareParams(self):
        """
        Generate the MathProg code for the declaration of params
        """
        graph = self._generateGraph()
        topological_order = sort_topologically_stackless(graph)

        if len(self.Params) > 0:
            paramStr = ""
            for paramIn in topological_order:
                if len(self.Params[paramIn]["sub-indices"]) == 0:
                    paramStr += "param " + paramIn
                else:
                    tupleVal = self._getTuple(self.Params[paramIn]["sub-indices"])

                    if tupleVal != None:
                        domain = "("+",".join(self.Tuples[tupleVal]["tuple"]) + ") " + self.Tuples[tupleVal]["op"] + " " + tupleVal
                    else:
                        domain = ", ".join(map(self._getParamDomain, self.Params[paramIn]["sub-indices"]))

                    if domain:
                        paramStr += "param " + paramIn + "{" + domain + "}"
                    else:
                        paramStr += "param " + paramIn

                if paramIn in self.Types and self.Types[paramIn]:
                    paramStr += " " + self.Types[paramIn]

                paramStr += ";\n"

            return paramStr
        else:
            return ""

    def _declareData(self):
        res = "data;\n\n"
        
        if len(self.Sets) > 0:
            for setIn in self.Sets:
                if not setIn in self.Params:
                    res += "set " + setIn + " :=;\n"

        res += "\n"

        if len(self.Params) > 0:
            for paramIn in self.Params:
                res += "param " + paramIn + " :=;\n"

        res += "\n"

        return res

    # Linear Program
    def _preModel(self):
        return self._declareSets() + "\n" + self._declareParams() + "\n" + self._declareVars() + "\n"

    def _posModel(self):
        res = "\nsolve;\n\n\n"
        res += self._declareData()
        res += "\nend;\n"

        return res

    def generateCode_LinearProgram(self, node):
        if node.constraints:
            return self._preModel() + "\n" + node.objective.generateCode(self) + "\n" + node.constraints.generateCode(self) + "\n" + self._posModel() + "\n"
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
        return "\n".join(map(self._getCodeConstraint, node.constraints))

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
        return node.linearExpression.generateCode(self) + ", " + node.op + " " + node.numericExpression1.generateCode(self) + ", " + node.op + " " + node.numericExpression2.generateCode(self)

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
        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = ", ".join(indexing)

        if node.logicalExpression:
            res += " : " + node.logicalExpression.generateCode(self)

        return res
    
    # Entry Indexing Expression
    def generateCode_EntryIndexingExpressionWithSet(self, node):
        if node.isBinary or node.isInteger or node.isNatural or node.isReal or Utils._isInstanceOfStr(node.variable):
            return ""
        elif isinstance(node.variable, ValueList):
            return ", ".join(map(lambda var: var.generateCode(self) + " " + node.op + " " + str(node.setExpression), node.variable.getValues()))
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

        return  var_gen + "[" + node.indices.generateCode(self) + "]"

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
