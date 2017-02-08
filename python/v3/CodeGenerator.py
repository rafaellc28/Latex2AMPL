from Utils import *
from ValueList import *
from Constraints import *
from SetExpression import *
from EntryIndexingExpression import *
from SymbolicExpression import *
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
from GenDeclarations import *
from GenDeclaration import *
from GenBelongsToList import *
from GenBelongsTo import *
from Constants import *

class CodeGenerator:
    """ Visitor in the Visitor Pattern """
    
    def __init__(self):
        self.genSets = GenSets()
        self.genVariables = GenVariables()
        self.genParameters = GenParameters()
        self.genDomains = GenDomains()
        self.genTypes = GenTypes()
        self.genTuples = GenTuples()
        self.genDeclarations = GenDeclarations()
        self.genBelongsToList = GenBelongsToList()
        self.genIndexingExpressionConstraints = GenList()
        self.genValueAssigned = GenList()
        self.genNames = GenList()
        self.topological_order = []

        self.totalObjectives = 0
        self.objectiveNumber = 0
        self.constraintNumber = 0
        self.stmtIndex = 0

        self.varNameSubIndices = []

    # from http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python
    def flatten(self, x):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(self.flatten(el))
            else:
                result.append(el)
        return result

    def generateCode(self, node):
        cls = node.__class__
        method_name = 'generateCode_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    def _getBiggestOrderInStmtFrom(self, _subIndices):
        orderInStmt = 0
        for _s in _subIndices:
            if _s.getOrderInStmt() > orderInStmt:
                orderInStmt = _s.getOrderInStmt()

        return orderInStmt

    def _getLogicalExpressionFromDeclaration(self, declaration, varName, _tuples, _subIndices):
        if declaration == None or declaration.getIndexingExpression() == None or declaration.getIndexingExpression().logicalExpression == None:
            return None

        logicalExpression = declaration.getIndexingExpression().logicalExpression
        self.genNames = GenList()
        logExpr = logicalExpression.generateCode(self)
        names = self.genNames.getAll()
        names = map(lambda el: el.getName(), names)

        if varName in names:
            return logExpr

        namesSet = set(names)

        tupleListAux = map(lambda el: el.getTupleVal(), _tuples)
        tupleListAux = self.flatten(tupleListAux)
        tupleListAux = list(namesSet.intersection(set(tupleListAux)))
        if len(tupleListAux) > 0:
            return logExpr

        subIndicesAux = map(lambda el: el.getName(), _subIndices)
        subIndicesAux = self.flatten(subIndicesAux)
        subIndicesAux = list(namesSet.intersection(set(subIndicesAux)))
        if len(subIndicesAux) > 0:
            return logExpr

        return None

    def _addDependences(self, value, stmtIndex, dependences):
        self.genNames = GenList()
        value.generateCode(self)

        names = self.genNames.getAll()
        if names != None and len(names) > 0:
            for name in names:
                if not self.genBelongsToList.has(GenBelongsTo(name.getName(), stmtIndex)):
                    dependences.append(name.getName())

    def _getDependences(self, paramIn):
        dependences = []

        decl = self.genDeclarations.get(paramIn.getName())
        if decl != None:
            value = decl.getValue()
            if value != None:
                self._addDependences(value.attribute, decl.getStmtIndex(), dependences)

            value = decl.getDefault()
            if value != None:
                self._addDependences(value.attribute, decl.getStmtIndex(), dependences)

            ins = decl.getIn()
            if ins != None and len(ins) > 0:
                for pSet in ins:
                    self._addDependences(pSet.attribute, decl.getStmtIndex(), dependences)

            withins = decl.getWithin()
            if withins != None and len(withins) > 0:
                for pSet in withins:
                    self._addDependences(pSet.attribute, decl.getStmtIndex(), dependences)

            relations = decl.getRelations()
            if relations != None and len(relations) > 0:
                for pRel in relations:
                    self._addDependences(pRel.attribute, decl.getStmtIndex(), dependences)

            idxExpression = decl.getIndexingExpression()
            if idxExpression != None:
                self._addDependences(idxExpression, decl.getStmtIndex(), dependences)

        return dependences

    def _getSubIndicesDomains(self, paramIn, stmtIndexInitial = None):

        useTestInitial = False
        testInitial = False
        firstStmt = int(paramIn.getFirstStmt())
        lastStmt =  int(paramIn.getLastStmt())
        
        if stmtIndexInitial != None and isinstance(int(stmtIndexInitial), int):
            stmtIndex = int(stmtIndexInitial)
            testInitial = True
            useTestInitial = True
        else:
            stmtIndex = lastStmt

        domain = ""

        while domain == "" and stmtIndex >= firstStmt:

            if useTestInitial and not testInitial and stmtIndex == stmtIndexInitial:
                break

            domains = {}
            _tuplesRet = []
            subIdxDomainsRet = []

            _subIndicesAllOrders = paramIn.getSubIndices().getAllSortedByOrder(lambda el: el.getStmtIndex() == stmtIndex)

            _subIndicesAll = {}
            for _subIndicesOrder in _subIndicesAllOrders:
                order = _subIndicesOrder.getOrder()

                if not order in _subIndicesAll:
                    _subIndicesAll[order] = []

                _subIndicesAll[order].append(_subIndicesOrder)

            for order in sorted(_subIndicesAll.iterkeys(), reverse=True):
                
                _subIndices = _subIndicesAll[order]
                _subIndices = sorted(_subIndices, key = lambda el: el.getIndice())

                idx = 0
                totalSubIndices = len(_subIndices)
                indexes = range(totalSubIndices)
                _subIndicesRemaining = list(_subIndices)

                while idx < totalSubIndices:
                    _combIndices = _subIndices[idx:]
                    _tuple = self._getTuple(paramIn, _combIndices, stmtIndex)

                    while _tuple == None and len(_combIndices) > 0:
                        _combIndices = _combIndices[:-1];
                        _tuple = self._getTuple(paramIn, _combIndices, stmtIndex)
                    
                    if _tuple != None:
                        domains[idx] = "(" + ",".join(_tuple.getTupleVal()) + ") " + _tuple.getOp() + " " + _tuple.getName()
                                            
                        for i in range(idx, idx+len(_combIndices)):
                            indexes.remove(i)

                        idx += len(_combIndices)

                        _tuplesRet.append(_tuple)

                        for _comb in _combIndices:
                            _subIndicesRemaining.remove(_comb)

                    else:
                        idx += 1

                if len(indexes) > 0:
                    _subIndices = _subIndicesRemaining
                    orderInStmt = self._getBiggestOrderInStmtFrom(_subIndices)
                    subIdxDomains = [self._getDomain(_subIndice, stmtIndex, orderInStmt) for _subIndice in _subIndices]
                    
                    if len(subIdxDomains) > 0 and all(subIdxDomains):
                        subIdxDomainsRet = subIdxDomains

                        self.varNameSubIndices = []
                        subIdxDomains = [self._getDomainStr(_subIndice, stmtIndex, orderInStmt) for _subIndice in _subIndices]

                        indexes = sorted(indexes)
                        for subIdxDomain in subIdxDomains:
                            domains[indexes.pop(0)] = subIdxDomain

                    else:
                        domains = {}

                domains_str = []
                if len(domains) > 0:
                    for key in sorted(domains.iterkeys()):
                        if domains[key] != None:
                            domains_str.append(domains[key])

                domain += ", ".join(domains_str)

                if domain != "":
                    break

            if domain != "":
                break

            if testInitial:
                testInitial = False
                stmtIndex = lastStmt+1

            stmtIndex -= 1
            
        return domain, stmtIndex, _tuplesRet, subIdxDomainsRet

    def _checkAddDependence(self, genObj, genObjOther, graph, name, dep):
        return dep != name and (genObj.has(dep) or genObjOther.has(dep)) and not dep in graph[name]

    def _generateGraphAux(self, graph, genObj, genObjOther):
        if len(genObj) > 0:
            for paramIn in genObj.getAll():
                name = paramIn.getName()
                if not name in graph:
                    graph[name] = []

                dependences = self._getDependences(paramIn)

                if len(dependences) > 0:
                    for dep in dependences:
                        if self._checkAddDependence(genObj, genObjOther, graph, name, dep):
                            graph[name].append(dep)

                if len(paramIn.getSubIndices()) > 0:
                    
                    _domain, stmtIndex, _tuples, subIdxDomains = self._getSubIndicesDomains(paramIn)

                    if _tuples != None and len(_tuples):
                        dependences = []
                        for _tuple in _tuples:
                            self._addDependences(_tuple.getTupleObj(), stmtIndex, dependences)

                        if len(dependences) > 0:
                            for dep in dependences:
                                if self._checkAddDependence(genObj, genObjOther, graph, name, dep):
                                    graph[name].append(dep)


                    if subIdxDomains != None and len(subIdxDomains) > 0 and all(subIdxDomains):
                        dependences = []
                        for _domain in subIdxDomains:
                            if isinstance(_domain, GenDomain):
                                self._addDependences(_domain.getDomainObj(), stmtIndex, dependences)

                                if _domain.getDomainSupObj() != None:
                                    self._addDependences(_domain.getDomainSupObj(), stmtIndex, dependences)

                            elif ".." in _domain:
                                param = _domain.split("..")

                                if param and param[0] and self._checkAddDependence(genObj, genObjOther, graph, name, param[0]):
                                    graph[name].append(param[0])

                                if param and param[1] and self._checkAddDependence(genObj, genObjOther, graph, name, param[1]):
                                    graph[name].append(param[1])

                            else:
                                param = _domain.split("[")
                                if param and param[0] and self._checkAddDependence(genObj, genObjOther, graph, name, param[0]):
                                    graph[name].append(param[0])

                        if len(dependences) > 0:
                            for dep in dependences:
                                if self._checkAddDependence(genObj, genObjOther, graph, name, dep):
                                    graph[name].append(dep)

    # Auxiliary Methods
    def _generateGraph(self):
        graph = {}

        self._generateGraphAux(graph, self.genSets, self.genParameters)
        self._generateGraphAux(graph, self.genParameters, self.genSets)

        return graph

    # Get the MathProg code for a given relational expression
    def _getCodeValue(self, value):
        val = value.generateCode(self)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given sub-indice
    def _getCodeID(self, id_):
        if isinstance(id_, ValuedNumericExpression):
            if isinstance(id_.value, Variable):
                id_.value.setIsSubIndice(True)

        elif isinstance(id_, Variable):
            id_.setIsSubIndice(True)

        val = id_.generateCode(self)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given objective
    def _getCodeObjective(self, objective):
        self.objectiveNumber += 1
        return objective.generateCode(self)

    # Get the MathProg code for a given constraint
    def _getCodeConstraint(self, constraint):
        if isinstance(constraint, Constraint):
            self.constraintNumber += 1
            return "s.t. C" + str(self.constraintNumber) + " " + constraint.generateCode(self)

        return ""

    # Get the MathProg code for a given entry
    def _getCodeEntry(self, entry): return entry.generateCode(self)

    # Get the MathProg code for a given entry
    def _getCodeEntryByKey(self, entry):
        for key in entry:
            return key, entry[key].generateCode(self)

    def _getDomainByOrder(self, var, stmtIndex, order):
        _domain = self.genDomains.get(GenDomain(var.getName(), stmtIndex, order))
        order_test = order

        while (_domain == None or _domain.getDomain() == None) and order_test >= 1:
            order_test -= 1
            _domain = self.genDomains.get(GenDomain(var.getName(), stmtIndex, order_test))

        if _domain == None or _domain.getDomain() == None:

            order_test = order
            lastOrder = self.genDomains.getBiggestOrderByNameAndStmt(var.getName(), stmtIndex)
            
            while (_domain == None or _domain.getDomain() == None) and order_test <= lastOrder:
                order_test += 1
                _domain = self.genDomains.get(GenDomain(var.getName(), stmtIndex, order_test))
        
        return _domain

    def _getDomain(self, var, stmtIndex, order):
        _domain = self._getDomainByOrder(var, stmtIndex, order)

        if _domain != None and _domain.getDomain() != None:
            return _domain

        elif var.getMinVal() < float('inf'):
            return str(var.getMinVal()) + ".." + str(var.getMaxVal())

        else:
            return ""


    def _getDomainStr(self, var, stmtIndex, order):
        _domain = self._getDomainByOrder(var, stmtIndex, order)

        if _domain != None and _domain.getDomain() != None:
            res = ""
            if not var.getName() in self.varNameSubIndices:
                res += var.getName() + " in "
                self.varNameSubIndices.append(var.getName())

            res += _domain.getDomain()

            return res

        elif var.getMinVal() < float('inf'):
            res = ""
            if isinstance(var.getName(), str) and not var.getName() in self.varNameSubIndices:
                res += var.getName() + " in "
                self.varNameSubIndices.append(var.getName())

            res += str(var.getMinVal()) + ".." + str(var.getMaxVal())

            return res

        else:
            return ""

    def _getTuple(self, variable, sub_indices, stmtIndex = None):
        """
        Get a tuple with sub-indices
        """
        subIndices = list(map(lambda var: var.getName(), sub_indices))

        _tupleRes = None
        for _tuple in self.genTuples.getAll():
            
            if subIndices == list(_tuple.getTupleVal()):
                if stmtIndex != None and stmtIndex == int(_tuple.getStmtIndex()):
                    return _tuple

                if variable.getLastStmt() == str(_tuple.getStmtIndex()):
                    return _tuple

                _tupleRes = _tuple

        if stmtIndex != None:
            return None

        return _tupleRes

    def _declareVars(self):
        """
        Generate the MathProg code for the declaration of variables
        """
        varStr = ""
        if len(self.genVariables) > 0:
            
            for var in self.genVariables.getAll():
                if not self.genParameters.has(var) and not self.genSets.has(var):
                    varStr += "var " + var.getName()
                    domain = None
                    _type = None

                    varDecl = self.genDeclarations.get(var.getName())

                    _subIndices = var.getSubIndices().getAllSortedByIndice()
                    
                    if len(_subIndices) > 0:
                        domain, stmtIndex, _tuple, subIdxDomains = self._getSubIndicesDomains(var, None if varDecl == None else varDecl.getStmtIndex())
                        if domain != "" and domain.strip() != "":
                            logical = self._getLogicalExpressionFromDeclaration(varDecl, var.getName(), _tuple, subIdxDomains)
                            varStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"
                        
                        if not domain  and varDecl != None:
                            if varDecl.getIndexingExpression() != None:
                                domain = varDecl.getIndexingExpression().generateCode(self)
                                varStr += "{" + domain + "}"

                    if varDecl != None:
                        sets = map(lambda el: el.attribute.generateCode(self), varDecl.getIn())
                        binary = filter(lambda el: el == Constants.BINARY or el.replace(" ", "") == Constants.BINARY_0_1, sets)

                        if binary != None and len(binary) > 0:
                            _type = Constants.BINARY
                        else:
                            integer = filter(lambda el: el.startswith(Constants.INTEGER), sets)
                            if integer != None and len(integer) > 0:
                                _type = integer[-1]

                        if _type != None:
                            varStr += " " + _type

                    if _type == None:
                        _type = self.genTypes.get(var)
                        if _type != None and _type.getType().strip() != "":
                            varStr += " " + _type.getType()

                    if varDecl != None:
                        attr = varDecl.getRelationEqualTo()
                        if attr != None:
                            varStr += ", = " + attr.attribute.generateCode(self)

                        else:
                            attr = varDecl.getRelationLessThanOrEqualTo()
                            if attr != None:
                                varStr += ", <= " + attr.attribute.generateCode(self)

                            attr = varDecl.getRelationGreaterThanOrEqualTo()
                            if attr != None:
                                varStr += ", >= " + attr.attribute.generateCode(self)

                    varStr += ";\n\n"

        return varStr

    def _declareSets(self):
        """
        Generate the MathProg code for the declaration of sets
        """
        setStr = ""
        if len(self.genSets) > 0:
            
            for setIn in self.genSets.getAll():
                if not self.genParameters.has(setIn):
                    setStr += "set " + setIn.getName()
                    domain = None
                    dimen = None

                    varDecl = self.genDeclarations.get(setIn.getName())

                    _subIndices = setIn.getSubIndices().getAllSortedByIndice()
                    if len(_subIndices) > 0:
                        domain, stmtIndex, _tuple, subIdxDomains = self._getSubIndicesDomains(var, None if varDecl == None else varDecl.getStmtIndex())
                        if domain != None and domain.strip() != "":
                            logical = self._getLogicalExpressionFromDeclaration(varDecl, setIn.getName(), _tuple, subIdxDomains)
                            setStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

                        if not domain and varDecl != None:
                            if varDecl.getIndexingExpression() != None:
                                domain = varDecl.getIndexingExpression().generateCode(self)
                                setStr += "{" + domain + "}"

                    if varDecl != None:
                        if varDecl.getDimen() != None:
                            dimen = varDecl.getDimen().attribute.generateCode(self)
                            setStr += " dimen " + dimen

                    if dimen == None:
                        if setIn.getDimension() > 1:
                            setStr += " dimen " + str(setIn.getDimension())

                    if varDecl != None:
                        subsets = varDecl.getWithin()
                        if subsets != None and len(subsets) > 0:
                            setStr += ", " + ",".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), subsets))

                        sets = varDecl.getIn()
                        if sets != None and len(sets) > 0:
                            sets = filter(lambda el: el != Constants.BINARY and el.replace(" ", "") != Constants.BINARY_0_1 and not el.startswith(Constants.INTEGER) and not el.startswith(Constants.REALSET) and not el.startswith(Constants.SYMBOLIC) and not el.startswith(Constants.LOGICAL), map(lambda el: el.attribute.generateCode(self), sets))
                            ins = ",".join(map(lambda el: "in " + el, sets))
                            
                            if ins != "":
                                setStr += ", " + ins

                        if varDecl.getDefault() != None:
                            default = ", default " + varDecl.getDefault().attribute.generateCode(self)
                            setStr += default

                        if varDecl.getValue() != None:
                            value = ", := " + varDecl.getValue().attribute.generateCode(self)
                            setStr += value
                            self.genValueAssigned.add(GenObj(setIn.getName()))

                    setStr += ";\n\n"

        return setStr

    def _declareParams(self):
        """
        Generate the MathProg code for the declaration of params
        """
        graph = self._generateGraph()
        self.topological_order = sort_topologically_stackless(graph)

        paramStr = ""
        if len(self.genParameters) > 0:

            for paramIn in self.topological_order:
                paramStr += "param " + paramIn
                domain = None
                _type = None

                varDecl = self.genDeclarations.get(paramIn)

                _genParameter = self.genParameters.get(paramIn)
                if len(_genParameter.getSubIndices()) > 0:
                    domain, stmtIndex, _tuple, subIdxDomains = self._getSubIndicesDomains(_genParameter, None if varDecl == None else varDecl.getStmtIndex())
                    if domain != None and domain.strip() != "":
                        logical = self._getLogicalExpressionFromDeclaration(varDecl, paramIn, _tuple, subIdxDomains)
                        paramStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

                    if not domain and varDecl != None:
                        if varDecl.getIndexingExpression() != None:
                            domain = varDecl.getIndexingExpression().generateCode(self)
                            paramStr += "{" + domain + "}"

                if varDecl != None:
                    sets = map(lambda el: el.attribute.generateCode(self), varDecl.getIn())
                    symbolic = filter(lambda el: el.startswith(Constants.SYMBOLIC), sets)

                    if symbolic != None and len(symbolic) > 0:
                        _type = Constants.SYMBOLIC
                    else:
                        logical = filter(lambda el: el.startswith(Constants.LOGICAL), sets)
                        
                        if logical != None and len(logical) > 0:
                            _type = Constants.LOGICAL
                        else:
                            binary = filter(lambda el: el == Constants.BINARY or el.replace(" ", "") == Constants.BINARY_0_1, sets)
                            if binary != None and len(binary) > 0:
                                _type = Constants.BINARY
                            else:
                                integer = filter(lambda el: el.startswith(Constants.INTEGER), sets)
                                if integer != None and len(integer) > 0:
                                    _type = integer[-1]

                    if _type != None:
                        paramStr += " " + _type

                if _type == None:
                    _type = self.genTypes.get(paramIn)
                    if _type != None:
                        paramStr += " " + _type.getType()

                if varDecl != None:
                    sets = varDecl.getIn()
                    if sets != None and len(sets) > 0:
                        sets = filter(lambda el: el != Constants.BINARY and el.replace(" ", "") != Constants.BINARY_0_1 and not el.startswith(Constants.INTEGER) and not el.startswith(Constants.REALSET) and not el.startswith(Constants.SYMBOLIC) and not el.startswith(Constants.LOGICAL), map(lambda el: el.attribute.generateCode(self), sets))
                        ins = ",".join(map(lambda el: "in " + el, sets))
                        
                        if ins != "":
                            paramStr += ", " + ins

                    relations = varDecl.getRelations()
                    if relations != None and len(relations) > 0:
                        paramStr += ", " + ",".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), relations))

                    if varDecl.getDefault() != None:
                        default = ", default " + varDecl.getDefault().attribute.generateCode(self)
                        paramStr += default

                    if varDecl.getValue() != None:
                        value = ", := " + varDecl.getValue().attribute.generateCode(self)
                        paramStr += value
                        self.genValueAssigned.add(GenObj(paramIn))

                paramStr += ";\n\n"

        return paramStr

    def _declareParam(self, _genParameter):
        paramStr = ""
        paramIn = _genParameter.getName()
        paramStr += "param " + paramIn
        domain = None
        _type = None

        varDecl = self.genDeclarations.get(_genParameter.getName())

        if len(_genParameter.getSubIndices()) > 0:
            domain, stmtIndex, _tuple, subIdxDomains = self._getSubIndicesDomains(_genParameter, None if varDecl == None else varDecl.getStmtIndex())
            if domain != None and domain.strip() != "":
                logical = self._getLogicalExpressionFromDeclaration(varDecl, paramIn, _tuple, subIdxDomains)
                paramStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

            if not domain and varDecl != None:
                if varDecl.getIndexingExpression() != None:
                    domain = varDecl.getIndexingExpression().generateCode(self)
                    paramStr += "{" + domain + "}"

        if varDecl != None:
            sets = map(lambda el: el.attribute.generateCode(self), varDecl.getIn())
            symbolic = filter(lambda el: el.startswith(Constants.SYMBOLIC), sets)

            if symbolic != None and len(symbolic) > 0:
                _type = Constants.SYMBOLIC
            else:
                logical = filter(lambda el: el.startswith(Constants.LOGICAL), sets)

                if logical != None and len(logical) > 0:
                    _type = Constants.LOGICAL
                else:
                    binary = filter(lambda el: el == Constants.BINARY or el.replace(" ", "") == Constants.BINARY_0_1, sets)
                    if binary != None and len(binary) > 0:
                        _type = Constants.BINARY
                    else:
                        integer = filter(lambda el: el.startswith(Constants.INTEGER), sets)
                        if integer != None and len(integer) > 0:
                            _type = integer[-1]

            if _type != None:
                paramStr += " " + _type

        if _type == None:
            _type = self.genTypes.get(paramIn)
            if _type != None:
                paramStr += " " + _type.getType()

        if varDecl != None:
            sets = varDecl.getIn()
            if sets != None and len(sets) > 0:
                sets = filter(lambda el: el != Constants.BINARY and el.replace(" ", "") != Constants.BINARY_0_1 and not el.startswith(Constants.INTEGER) and not el.startswith(Constants.REALSET) and not el.startswith(Constants.SYMBOLIC) and not el.startswith(Constants.LOGICAL), map(lambda el: el.attribute.generateCode(self), sets))
                ins = ",".join(map(lambda el: "in " + el, sets))

                if ins != "":
                    paramStr += ", " + ins

            relations = varDecl.getRelations()
            if relations != None and len(relations) > 0:
                paramStr += ", " + ",".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), relations))

            if varDecl.getDefault() != None:
                default = ", default " + varDecl.getDefault().attribute.generateCode(self)
                paramStr += default

            if varDecl.getValue() != None:
                value = ", := " + varDecl.getValue().attribute.generateCode(self)
                paramStr += value
                self.genValueAssigned.add(GenObj(paramIn))

        paramStr += ";\n\n"

        return paramStr

    def _declareSet(self, _genSet):
        setStr = ""

        setStr += "set " + _genSet.getName()
        domain = None
        dimen = None

        varDecl = self.genDeclarations.get(_genSet.getName())

        if len(_genSet.getSubIndices()) > 0:
            domain, stmtIndex, _tuple, subIdxDomains = self._getSubIndicesDomains(_genSet, None if varDecl == None else varDecl.getStmtIndex())
            if domain != None and domain.strip() != "":
                logical = self._getLogicalExpressionFromDeclaration(varDecl, _genSet.getName(), _tuple, subIdxDomains)
                setStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

            if not domain and varDecl != None:
                if varDecl.getIndexingExpression() != None:
                    domain = varDecl.getIndexingExpression().generateCode(self)
                    setStr += "{" + domain + "}"

        if varDecl != None:
            if varDecl.getDimen() != None:
                dimen = varDecl.getDimen().attribute.generateCode(self)
                setStr += " dimen " + dimen

        if dimen == None:
            if _genSet.getDimension() > 1:
                setStr += " dimen " + str(_genSet.getDimension())

        if varDecl != None:
            subsets = varDecl.getWithin()
            if subsets != None and len(subsets) > 0:
                setStr += ", " + ",".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), subsets))

            sets = varDecl.getIn()
            if sets != None and len(sets) > 0:
                sets = filter(lambda el: el != Constants.BINARY and el.replace(" ", "") != Constants.BINARY_0_1 and not el.startswith(Constants.INTEGER) and not el.startswith(Constants.REALSET) and not el.startswith(Constants.SYMBOLIC) and not el.startswith(Constants.LOGICAL), map(lambda el: el.attribute.generateCode(self), sets))
                ins = ",".join(map(lambda el: "in " + el, sets))
                
                if ins != "":
                    setStr += ", " + ins
            
            if varDecl.getDefault() != None:
                default = ", default " + varDecl.getDefault().attribute.generateCode(self)
                setStr += default

            if varDecl.getValue() != None:
                value = ", := " + varDecl.getValue().attribute.generateCode(self)
                setStr += value
                self.genValueAssigned.add(GenObj(_genSet.getName()))

        setStr += ";\n\n"

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
        res = ""
        
        if len(self.genSets) > 0:
            for setIn in self.genSets.getAll():
                if not self.genValueAssigned.has(setIn.getName()) and not self.genParameters.has(setIn):
                    if len(setIn.getSubIndices()) > 0:
                        dimenIdx = "[" + ",".join(["0"] * len(setIn.getSubIndices().getAllSortedByOrder(lambda el: el.getStmtIndex() == setIn.getLastStmt() and el.getOrder() == 0))) + "]"
                    else:
                        dimenIdx = ""

                    res += "set " + setIn.getName() + dimenIdx + " :=;\n\n"

        if res != "":
            res += "\n"

        if len(self.genParameters) > 0:
            for paramIn in self.topological_order:
                if not self.genValueAssigned.has(paramIn):
                    _genParameter = self.genParameters.get(paramIn)
                    
                    value = ""
                    if len(_genParameter.getSubIndices()) == 0:
                        if _genParameter.getIsSymbolic():
                            value += " ''"
                        else:
                            value += " 0"

                    res += "param " + paramIn + " :=" + value + ";\n\n"

        if res != "":
            res = "data;\n\n" + res + "\n"

        return res

    def _declareDataParam(self, _genParameter):
        res = ""

        if not self.genValueAssigned.has(_genParameter.getName()):
            value = ""

            if len(_genParameter.getSubIndices()) == 0:
                if _genParameter.getIsSymbolic():
                    value += " ''"
                else:
                    value += " 0"

            res += "param " + _genParameter.getName() + " :=" + value + ";\n\n"

        return res

    def _declareDataSet(self, _genSet):
        res = ""

        if not self.genValueAssigned.has(_genSet.getName()):
            if len(_genSet.getSubIndices()) > 0:
                dimenIdx = "[" + ",".join(["0"] * len(_genSet.getSubIndices().getAllSortedByOrder(lambda el: str(el.getStmtIndex()) == _genSet.getLastStmt() and el.getOrder() == 0))) + "]"
            else:
                dimenIdx = ""

            res += "set " + _genSet.getName() + dimenIdx + " :=;\n\n"

        return res

    def _declareDataSetsAndParams(self):
        res = ""

        if len(self.topological_order) > 0:
            for paramSetIn in self.topological_order:
                _genObj = self.genParameters.get(paramSetIn)

                if _genObj != None:
                    res += self._declareDataParam(_genObj)
                else:
                    _genObj = self.genSets.get(paramSetIn)

                    if _genObj != None:
                        res += self._declareDataSet(_genObj)

        if res != "":
            res = "data;\n\n" + res + "\n"

        return res

    def _preModel(self):
        res = ""

        setsAndParams = self._declareSetsAndParams()
        if setsAndParams != "":
            res += setsAndParams

        variables = self._declareVars()
        if variables != "":
            if res != "":
                res += "\n"

            res += variables

        return res
    
    def _posModel(self):
        res = "\nsolve;\n\n\n"
        #res += self._declareData()
        res += self._declareDataSetsAndParams()
        res += "end;"

        return res

    def generateCode_Main(self, node):
        return node.problem.generateCode(self)

    def generateCode_LinearEquations(self, node):
        preModel = self._preModel()
        if preModel != "":
            preModel += "\n"

        return preModel + node.constraints.generateCode(self) + "\n\n" + self._posModel()

    def generateCode_LinearProgram(self, node):
        preModel = self._preModel()
        if preModel != "":
            preModel += "\n"

        res = preModel + node.objective.generateCode(self) + "\n\n"

        if node.constraints:
            res += node.constraints.generateCode(self) + "\n\n"
        
        if node.declarations:
            res += node.declarations.generateCode(self) + "\n\n"

        res += self._posModel()

        return res

    # Objectives
    def generateCode_Objectives(self, node):
        self.totalObjectives = len(node.objectives)
        return "\n\n".join(map(self._getCodeObjective, node.objectives))

    # Objective Function
    def generateCode_Objective(self, node):
        """
        Generate the code in MathProg for this Objective
        """
        
        domain_str = ""
        if node.domain:
            idxExpression = node.domain.generateCode(self)
            if idxExpression:
                domain_str = " {" + idxExpression + "}"

        return node.type + " obj" + (str(self.objectiveNumber) if self.totalObjectives > 1 else "")  + domain_str + ": " + node.linearExpression.generateCode(self) + ";"

    # Constraints
    def generateCode_Constraints(self, node):
        return "\n\n".join(filter(lambda el: el != "" and el != None, map(self._getCodeConstraint, node.constraints)))

    def generateCode_Constraint(self, node):
        res = ""

        if node.indexingExpression:
            idxExpression = node.indexingExpression.generateCode(self)

            if idxExpression.strip() != "":
                res += "{" + idxExpression + "} :\n\t"
            else:
                res += " : "    
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

        res += node.linearExpression.generateCode(self)

        return res

    def generateCode_ConditionalLinearExpression(self, node):
        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.linearExpression1.generateCode(self)

        if node.linearExpression2:
            res += " else " + node.linearExpression2.generateCode(self)

        return res

    # Numeric Expression
    def generateCode_NumericExpressionWithFunction(self, node):
        res = str(node.function) + "("

        if node.numericExpression1 != None:
            res += node.numericExpression1.generateCode(self)

        if node.numericExpression2 != None:
            res += ", " + node.numericExpression2.generateCode(self)

        res += ")"

        return res

    def generateCode_ValuedNumericExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_NumericExpressionBetweenParenthesis(self, node):
        return "(" + node.numericExpression.generateCode(self) + ")"

    def generateCode_NumericExpressionWithArithmeticOperation(self, node):
        res = node.numericExpression1.generateCode(self) + " " + node.op + " "

        if node.op == NumericExpressionWithArithmeticOperation.POW and not (isinstance(node.numericExpression2, ValuedNumericExpression) or isinstance(node.numericExpression2, NumericExpressionBetweenParenthesis)):
            res += "(" + node.numericExpression2.generateCode(self) + ")"
        else:
            res += node.numericExpression2.generateCode(self)

        return res

    def generateCode_MinusNumericExpression(self, node):
        return "-" + node.numericExpression.generateCode(self)

    def generateCode_IteratedNumericExpression(self, node):
        if node.supNumericExpression:
            res = str(node.op) + "{" + node.indexingExpression.generateCode(self) + "..(" + node.supNumericExpression.generateCode(self) + ")}"
        else:
            res = str(node.op) + "{" + node.indexingExpression.generateCode(self) + "}"

        res += node.numericExpression.generateCode(self)

        return res

    def generateCode_ConditionalNumericExpression(self, node):
        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.numericExpression1.generateCode(self)

        if node.numericExpression2:
            res += " else " + node.numericExpression2.generateCode(self)

        return res

    # Symbolic Expression
    def generateCode_SymbolicExpressionWithFunction(self, node):
        res = str(node.function) + "("
        if node.function == SymbolicExpressionWithFunction.SUBSTR:
            res += node.symbolicExpression.generateCode(self) + "," + node.numericExpression1.generateCode(self)
            if node.numericExpression2 != None:
                res += "," + node.numericExpression2.generateCode(self)
        
        elif node.function == SymbolicExpressionWithFunction.TIME2STR:
            res += node.numericExpression1.generateCode(self) + "," + node.symbolicExpression.generateCode(self)

        res += ")"

        return res

    def generateCode_StringSymbolicExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_SymbolicExpressionBetweenParenthesis(self, node):
        return "(" + node.symbolicExpression.generateCode(self) + ")"

    def generateCode_SymbolicExpressionWithOperation(self, node):
        return node.symbolicExpression1.generateCode(self) + " " + node.op + " " + node.symbolicExpression2.generateCode(self)

    def generateCode_ConditionalSymbolicExpression(self, node):
        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.symbolicExpression1.generateCode(self)

        if node.symbolicExpression2 != None:
            res += " else " + node.symbolicExpression2.generateCode(self)

        return res

    # Indexing Expression
    def generateCode_IndexingExpression(self, node):
        #entrySets = []
        #for entry in node.entriesIndexingExpression:
        #    if isinstance(entry, EntryIndexingExpressionWithSet):
        #        entrySets.append(entry.setExpression.generateCode(self))

        #entrySetsTopologicalOrder = [elem for elem in self.topological_order if elem in entrySets]

        #entries = node.entriesIndexingExpression
        #entriesNew = []

        #for entrySet in entrySetsTopologicalOrder:
        #    entriesToRemove = []
        #    for entry in entries:
        #        if isinstance(entry, EntryIndexingExpressionWithSet):
        #            if entry.setExpression.generateCode(self) == entrySet:
        #                entriesNew.append(entry)
        #                entriesToRemove.append(entry)
            
        #    for entry in entriesToRemove:
        #        entries.remove(entry)

        #for entry in entries:
        #    entriesNew.append(entry)

        #indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, entriesNew))
        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = ", ".join(indexing)

        if node.logicalExpression:
            res += " : " + node.logicalExpression.generateCode(self)

        return res
    
    # Entry Indexing Expression
    def generateCode_EntryIndexingExpressionWithSet(self, node):
        if node.isBinary or node.isInteger or node.isNatural or node.isReal or node.isSymbolic or node.isLogical or Utils._isInstanceOfStr(node.variable):
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

    def generateCode_EntryLogicalExpressionNot(self, node):
        return "not " + node.logicalExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionNumericOrSymbolic(self, node):
        return node.numericOrSymbolicExpression.generateCode(self)

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

        return  var_gen

    def generateCode_SetExpressionWithOperation(self, node):
        return node.setExpression1.generateCode(self) + " " + node.op + " " + node.setExpression2.generateCode(self)

    def generateCode_SetExpressionBetweenBraces(self, node):
        if node.setExpression != None:
            setExpression = node.setExpression.generateCode(self)
        else:
            setExpression = ""

        return "{" + setExpression + "}"

    def generateCode_SetExpressionBetweenParenthesis(self, node):
        return "(" + node.setExpression.generateCode(self) + ")"

    def generateCode_IteratedSetExpression(self, node):
        integrands = ""
        if node.integrands != None:
            if len(node.integrands) == 1:
                integrands += node.integrands[0].generateCode(self)
            else:
                integrands += "(" + ",".join(map(lambda el: el.generateCode(self), node.integrands)) + ")"

        return "setof {" + node.indexingExpression.generateCode(self) + "} " + integrands

    def generateCode_ConditionalSetExpression(self, node):
        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.setExpression1.generateCode(self)

        if node.setExpression2:
            res += " else " + node.setExpression2.generateCode(self)

        return res

    # Range
    def generateCode_Range(self, node):
        initValue = node.rangeInit.generateCode(self)
        initValue = Utils._getInt(initValue)

        endValue = node.rangeEnd.generateCode(self)
        endValue = Utils._getInt(endValue)

        res = initValue + ".." + endValue
        if node.by != None:
            res += " by " + node.by.generateCode(self)

        return res

    # Value List
    def generateCode_ValueList(self, node):
        return ",".join(map(self._getCodeValue, node.values))

    # Variable List
    def generateCode_VariableList(self, node):
        return ",".join(map(self._getCodeValue, node.variables))

    # Tuple
    def generateCode_Tuple(self, node):
        return "(" + ",".join(map(self._getCodeValue, node.values)) + ")"

    # Tuple List
    def generateCode_TupleList(self, node):
        return ",".join(map(self._getCodeValue, node.values))

    # Value
    def generateCode_Value(self, node):
        return node.value.generateCode(self)

    # Variable
    def generateCode_Variable(self, node):
        #if not node.isSubIndice and not node.isInSet:
        self.genNames.add(GenObj(node.generateCodeWithoutIndices(self)))

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

    # String
    def generateCode_String(self, node):
        return node.string
