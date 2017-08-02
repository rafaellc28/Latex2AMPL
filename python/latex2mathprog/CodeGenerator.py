from Utils import *
from ValueList import *
from Tuple import *
from Constraints import *
from SetExpression import *
from EntryIndexingExpression import *
from SymbolicExpression import *
from TopologicalSort import *
from GenSets import *
from GenVariables import *
from GenParameters import *
from GenDeclarations import *
from GenBelongsToList import *
from GenBelongsTo import *
from Constants import *
from SymbolTables import *

class CodeGenerator:
    """ Visitor in the Visitor Pattern """
    
    def __init__(self):
        self.genSets = GenSets()
        self.genVariables = GenVariables()
        self.genParameters = GenParameters()
        self.genDeclarations = GenDeclarations()
        self.genBelongsToList = GenBelongsToList()
        self.genValueAssigned = GenList()
        self.topological_order = []

        self.totalObjectives = 0
        self.objectiveNumber = 0
        self.constraintNumber = 0
        self.stmtIndex = 0

        self.symbolTables = None
        self.symbolTables = SymbolTables()

        self.parameters = []
        self.sets = []
        self.variables = []
        self.parameters_and_sets = []

        self.identifiers = {}

    def generateCode(self, node):
        cls = node.__class__
        method_name = 'generateCode_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    def init(self):
        self.parameters = map(lambda el: el.getName(), self.genParameters.getAll())
        self.sets = map(lambda el: el.getName(), self.genSets.getAll())
        self.variables = map(lambda el: el.getName(), self.genVariables.getAll())

        self.parameters_and_sets = self.parameters + self.sets
        
        if len(self.genVariables) > 0:
            for var in self.genVariables.getAll():
                if not self.genParameters.has(var) and not self.genSets.has(var):
                    domain, domain_list, dependencies, sub_indices = self._getSubIndicesDomains(var)
                    _types, dim, minVal, maxVal = self._getDomain(var)
                    self.identifiers[var.getName()] = {"types": _types,
                                                       "dim": dim,
                                                       "minVal": minVal,
                                                       "maxVal": maxVal,
                                                       "domain": domain, 
                                                       "domain_list": domain_list, 
                                                       "dependencies": dependencies, 
                                                       "sub_indices": sub_indices}

        if len(self.genParameters) > 0:
            for var in self.genParameters.getAll():
                domain, domain_list, dependencies, sub_indices = self._getSubIndicesDomains(var)
                _types, dim, minVal, maxVal = self._getDomain(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domain_list": domain_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices}

        if len(self.genSets) > 0:
            for var in self.genSets.getAll():
                domain, domain_list, dependencies, sub_indices = self._getSubIndicesDomains(var)
                _types, dim, minVal, maxVal = self._getDomain(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domain_list": domain_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices}

        '''
        print("Symbol Tables")
        self._printSymbolTables(self.symbolTables)
        print("")
        
        print("Declarations")
        declarations = self.symbolTables.getDeclarations()
        self._printSymbolTables(declarations.iteritems())
        print("")
        
        print("Leafs")
        self._printLeafs()
        print("")
        '''

    def _printTables(self, tables):
        for dictStmt in tables:
            print("SymbolTable Scope " + str(dictStmt["scope"]) + ". Level: " + str(dictStmt["level"]) + ". Leaf: " + str(dictStmt["table"].getIsLeaf()) + 
                  ". Parent Scope: " + (str(None) if dictStmt["table"].getParent() == None else str(dictStmt["table"].getParent().getScope())))

            print("\n".join([str(key) + ": type = " + str(value.getType()) + "; scope = " + str(value.getScope()) + 
                   "; properties = [name: " + str(value.getProperties().getName()) + ", domains: " + 
                   str(map(lambda el: "{" + str(el.getOp()) + " " + el.getName() + ", dependencies: " + str(el.getDependencies()) + "}", value.getProperties().getDomains())) + 
                   ", minVal: " + str(value.getProperties().getMinVal()) + ", maxVal: " + str(value.getProperties().getMaxVal()) + 
                   ", dimension: " + str(value.getProperties().getDimension()) + ", default: " + str(value.getProperties().getDefault()) + 
                   ", attributes: " + str(value.getProperties().getAttributes()) + "]; inferred = " + str(value.getInferred()) + 
                   "; sub_indices = " + str(value.getSubIndices()) + "; isDefined = " + str(value.getIsDefined()) + ";"
                   for key, value in dictStmt["table"]]))
            print("")

    def _printStatementSymbolTable(self, statement, tables):
        print("SymbolTable Stmt " + str(statement) + ". Declaration: " + str(tables["isDeclaration"]))
        self._printTables(tables["tables"])


    def _printLeafs(self):
        for stmt, tables in self.symbolTables:
            print("SymbolTable Stmt " + str(stmt) + ". Declaration: " + str(tables["isDeclaration"]))
            leafs = self.symbolTables.getLeafs(stmt)
            self._printTables(leafs)

    def _printSymbolTables(self, symbolTables):
        for stmt, tables in symbolTables:
            self._printStatementSymbolTable(stmt, tables)

    def _getLogicalExpressionOfDeclaration(self, declaration, varName, dependencies, sub_indices):
        if declaration == None or declaration.getIndexingExpression() == None or declaration.getIndexingExpression().logicalExpression == None:
            return None

        logicalExpression = declaration.getIndexingExpression().logicalExpression
        logicalExpressionDependencies = set(logicalExpression.getDependencies())

        if varName in logicalExpressionDependencies:
            return logicalExpression.generateCode(self)

        if len(logicalExpressionDependencies.intersection(sub_indices)) > 0:
            return logicalExpression.generateCode(self)

        if len(logicalExpressionDependencies.intersection(dependencies)) > 0:
            return logicalExpression.generateCode(self)

        return None

    def _getSubIndicesDomainsAndDependencies(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["domain"], res["domain_list"], res["dependencies"], res["sub_indices"]

        return None, [], [], []

    def _getProperties(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["types"], res["dim"], res["minVal"], res["maxVal"]

        return None, [], [], []

    def _getItemDomain(self, domains, totalIndices):
        size = len(domains)
        if size == 0:
            return None, None, None

        while size > 0:
            size -= 1
            domain = domains[size]
            dependencies = list(domain.getDependencies())

            if domain.getName() in dependencies:
                dependencies.remove(domain.getName())

            if len(dependencies) > 0:
                if not set(dependencies).issubset(set(totalIndices+self.parameters_and_sets)):
                    break

            deps = set(domain.getDependencies())
            deps.discard(set(totalIndices))

            return domain.getOp(), domain.getName(), list(deps)

        return None, None, None

    def _getDomainSubIndices(self, table, selectedIndices, totalIndices):
        if not isinstance(selectedIndices, str):
            selectedIndices = ",".join(selectedIndices)

        while table != None:
            value = table.lookup(selectedIndices)
            if value != None:
                op, domain, deps = self._getItemDomain(value.getProperties().getDomains(), totalIndices)

                if domain != None:
                    return op, domain, deps

            table = table.getParent()

        return None, None, None

    def _getSubIndicesDomainsByTables(self, name, tables, skip_outermost_scope = False):

        domain = ""
        domains_ret = []
        dependencies_ret = []
        sub_indices_ret = []

        for table in sorted(tables, key=lambda el: el["scope"], reverse=True):

            table = table["table"]

            while table != None:

                if skip_outermost_scope and table.getParent() == None:
                    break

                t = table.lookup(name)
                while t == None and table != None:
                    table = table.getParent()

                    if table != None:
                        t = table.lookup(name)

                if skip_outermost_scope and table != None and table.getParent() == None:
                    break

                if t == None:
                    continue

                sub_indices_list = list(t.getSubIndices())
                sub_indices_list.reverse()

                domains = {}
                dependencies = {}
                
                for _subIndices in sub_indices_list:
                    totalIndices = list(_subIndices)
                    idx = 0
                    totalSubIndices = len(_subIndices)
                    indexes = range(totalSubIndices)
                    _subIndicesRemaining = list(_subIndices)

                    while idx < totalSubIndices:
                        _combIndices = _subIndices[idx:]
                        
                        if len(_combIndices) <= 1:
                            idx += 1
                            continue

                        op, _tuple, deps = self._getDomainSubIndices(table, _combIndices, totalIndices)
                        while _tuple == None and len(_combIndices) > 0:
                            _combIndices = _combIndices[:-1];
                            
                            if len(_combIndices) <= 1:
                                break

                            op, _tuple, deps = self._getDomainSubIndices(table, _combIndices, totalIndices)
                            
                        if _tuple != None:
                            domains[idx] = "(" + ",".join(_combIndices) + ") " + op + " " + _tuple
                            dependencies[idx] = deps
                            
                            for i in range(idx, idx+len(_combIndices)):
                                indexes.remove(i)

                            idx += len(_combIndices)

                            for _comb in _combIndices:
                                _subIndicesRemaining.remove(_comb)

                        else:
                            idx += 1
                        
                    if len(indexes) > 0:
                        _subIndices = _subIndicesRemaining
                        subIdxDomains = [self._getDomainSubIndices(table, _subIndice, totalIndices) for _subIndice in _subIndices]
                        subIdxDomains = [d for d in subIdxDomains if d[1] != None]
                        
                        if len(subIdxDomains) == len(_subIndicesRemaining):

                            varNameSubIndices = []
                            indexes = sorted(indexes)
                            for i in range(len(subIdxDomains)):
                                ind = indexes.pop(0)
                                domains[ind] = (_subIndices[i] + " " + subIdxDomains[i][0] + " " if not _subIndices[i] in varNameSubIndices else "") + subIdxDomains[i][1]
                                dependencies[ind] = subIdxDomains[i][2]
                                varNameSubIndices.append(_subIndices[i])

                        else:
                            domains = {}
                            dependencies = {}

                    if domains:
                        break 
                
                if len(domains) > 0:
                    domains_str = []
                    domains_ret = []
                    dependencies_ret = []
                    sub_indices_ret = _subIndices

                    for key in sorted(domains.iterkeys()):
                        if domains[key] != None:
                            domains_str.append(domains[key])
                            domains_ret.append(domains[key])
                            dependencies_ret += dependencies[key]

                    domain += ", ".join(domains_str)

                if domain != "":
                    break

                table = table.getParent()

            if domain != "":
                break

        return domain, domains_ret, list(set(dependencies_ret)), sub_indices_ret


    def _getSubIndicesDomainsByStatements(self, name, statements):
        domain = ""
        domains = []
        dependencies = []
        sub_indices = []
        
        for stmt in sorted(statements, reverse=True):
            
            scopes = self.symbolTables.getFirstScopeByKey(name, stmt)
            domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByTables(name, scopes)

            if domain != "":
                break
            
            leafs = self.symbolTables.getLeafs(stmt)
            domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByTables(name, leafs, True)

            if domain != "":
                break

        return domain, domains, dependencies, sub_indices

    def _getSubIndicesDomains(self, identifier):
        name = identifier.getName()
        declarations = self.symbolTables.getDeclarationsWhereKeyIsDefined(name)
        domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByStatements(name, declarations)

        if domain == "":
            statements = self.symbolTables.getStatementsByKey(name)
            domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByStatements(name, statements)

        return domain, domains, dependencies, sub_indices


    def _getDomainsByTables(self, name, tables, _types, dim, minVal, maxVal, skip_outermost_scope = False):
        
        for table in sorted(tables, key=lambda el: el["scope"], reverse=True):

            table = table["table"]

            while table != None:

                if skip_outermost_scope and table.getParent() == None:
                    break

                t = table.lookup(name)
                while t == None and table != None:
                    table = table.getParent()

                    if table != None:
                        t = table.lookup(name)

                if skip_outermost_scope and table != None and table.getParent() == None:
                    break

                if t == None:
                    continue

                prop = t.getProperties()
                domains = prop.getDomains()

                for domain in domains:
                    inserted = False
                    for _type in _types:
                        if domain.getName() == _type.getName():
                            inserted = True # last occurrence prevails (it is scanning from bottom to top, right to left)
                            break

                    if not inserted:
                        _types.append(domain)

                if prop.getDimension() != None and prop.getDimension() > 1 and dim == None:
                    dim = prop.getDimension()

                if prop.getMinVal() != None:
                    if minVal == None or minVal > prop.getMinVal():
                        minVal = prop.getMinVal()

                if prop.getMaxVal() != None:
                    if maxVal == None or maxVal < prop.getMaxVal():
                        maxVal = prop.getMaxVal()

                table = table.getParent()

        return _types, dim, minVal, maxVal

    def _getDomainsByStatements(self, name, statements, _types, dim, minVal, maxVal):
        
        for stmt in sorted(statements, reverse=True):
            
            scopes = self.symbolTables.getFirstScopeByKey(name, stmt)
            _types, dim, minVal, maxVal = self._getDomainsByTables(name, scopes, _types, dim, minVal, maxVal, False)

            leafs = self.symbolTables.getLeafs(stmt)
            _types, dim, minVal, maxVal = self._getDomainsByTables(name, leafs, _types, dim, minVal, maxVal, True)

        return _types, dim, minVal, maxVal

    def _getDomain(self, identifier):
        _types = []
        dim = None
        minVal = None
        maxVal = None

        name = identifier.getName()
        declarations = self.symbolTables.getDeclarationsWhereKeyIsDefined(name)
        _types, dim, minVal, maxVal = self._getDomainsByStatements(name, declarations, _types, dim, minVal, maxVal)

        statements = self.symbolTables.getStatementsByKey(name)
        _types, dim, minVal, maxVal = self._getDomainsByStatements(name, statements, _types, dim, minVal, maxVal)

        return _types, dim, minVal, maxVal

   
    def _addDependences(self, value, stmtIndex, dependences):
        names = value.getDependencies()

        if names != None and len(names) > 0:
            for name in names:
                if not self.genBelongsToList.has(GenBelongsTo(name, stmtIndex)):
                    dependences.append(name)

    def _getDependences(self, identifier):
        dependences = []

        decl = self.genDeclarations.get(identifier.getName())
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

    def _checkAddDependence(self, graph, name, dep):
        return dep != name and not dep in graph[name] and dep in self.parameters_and_sets

    def _generateGraphAux(self, graph, genObj):
        if len(genObj) > 0:
            for identifier in genObj.getAll():
                
                name = identifier.getName()
                if not name in graph:
                    graph[name] = []
                
                dependences = self._getDependences(identifier)

                if len(dependences) > 0:
                    for dep in dependences:
                        if self._checkAddDependence(graph, name, dep):
                            graph[name].append(dep)

                _domain, domains_vec, dependencies_vec, sub_indices = self._getSubIndicesDomainsAndDependencies(identifier.getName())

                if len(dependencies_vec) > 0:
                    for dep in dependencies_vec:
                        if self._checkAddDependence(graph, name, dep):
                            graph[name].append(dep)

    # Auxiliary Methods
    def _generateGraph(self):
        
        graph = {}

        self._generateGraphAux(graph, self.genSets)
        self._generateGraphAux(graph, self.genParameters)

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
            if isinstance(id_.value, Identifier):
                id_.value.setIsSubIndice(True)

        elif isinstance(id_, Identifier):
            id_.setIsSubIndice(True)

        val = id_.generateCode(self)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given entry
    def _getCodeEntry(self, entry): return entry.generateCode(self)

    # Get the MathProg code for a given entry
    def _getCodeEntryByKey(self, entry):
        for key in entry:
            return key, entry[key].generateCode(self)

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

    def notInTypesThatAreNotDeclarable(self, value):
        if isinstance(value, Tuple):
            return True
        #print("before", str(value))
        value = value.getSymbol()
        #print("after", str(value))
        return not value.isBinary and not value.isInteger and not value.isNatural and not value.isReal and not value.isSymbolic and not \
        value.isLogical and not value.isDeclaredAsVar and not value.isDeclaredAsParam and not value.isDeclaredAsSet and not \
        isinstance(value, str)

    def _removeTypesThatAreNotDeclarable(self, _types):
        return filter(lambda el: not el.getName() in [Constants.VARIABLES, Constants.PARAMETERS, Constants.SETS], _types)

    def _removePreDefinedTypes(self, _types):
        return filter(lambda el: not el in [Constants.VARIABLES, Constants.PARAMETERS, Constants.SETS] and 
                        el != Constants.BINARY and el.replace(" ", "") != Constants.BINARY_0_1 and 
                        not el.startswith(Constants.INTEGER) and not el.startswith(Constants.REALSET) and 
                        not el.startswith(Constants.SYMBOLIC) and not el.startswith(Constants.LOGICAL), _types)

    def _getTypes(self, _types):
        return filter(lambda el: el.getName().startswith(Constants.BINARY) or el.getName().replace(" ", "") == Constants.BINARY_0_1 or el.getName().startswith(Constants.INTEGER) or el.getName().startswith(Constants.REALSET), _types)

    def _getModifiers(self, _types):
        return filter(lambda el: el.getName().startswith(Constants.LOGICAL) or el.getName().startswith(Constants.SYMBOLIC), _types)

    def _declareVars(self):
        """
        Generate the MathProg code for the declaration of identifiers
        """

        varStr = ""
        if len(self.genVariables) > 0:
            
            for var in self.genVariables.getAll():
                if not self.genParameters.has(var) and not self.genSets.has(var):
                    
                    varStr += "var " + var.getName()
                    domain = None
                    _type = None

                    varDecl = self.genDeclarations.get(var.getName())

                    domain, domains_vec, dependencies_vec, sub_indices_vec = self._getSubIndicesDomainsAndDependencies(var.getName())
                    _types, dim, minVal, maxVal = self._getProperties(var.getName())

                    if domain and domain.strip() != "":
                        logical = self._getLogicalExpressionOfDeclaration(varDecl, var.getName(), dependencies_vec, sub_indices_vec)
                        varStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"
                    
                    if not domain and varDecl != None:
                        if varDecl.getIndexingExpression() != None:
                            domain = varDecl.getIndexingExpression().generateCode(self)
                            varStr += "{" + domain + "}"

                    _types = self._removeTypesThatAreNotDeclarable(_types)
                    _types = self._getTypes(_types)

                    if len(_types) > 0:
                        _type = _types[0].getName()
                        _type = _type if _type != Constants.BINARY_0_1 else Constants.BINARY
                        _type = _type if not _type.startswith(Constants.REALSET) else _type[8:]

                        if _type.strip() != "":
                            varStr += " " + _type

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

    def _declareParam(self, _genParameter):
        paramStr = ""
        param = _genParameter.getName()
        paramStr += "param " + param
        domain = None
        _type = None

        varDecl = self.genDeclarations.get(_genParameter.getName())

        domain, domains_vec, dependencies_vec, sub_indices_vec = self._getSubIndicesDomainsAndDependencies(_genParameter.getName())
        _types, dim, minVal, maxVal = self._getProperties(_genParameter.getName())

        if domain != None and domain.strip() != "":
            logical = self._getLogicalExpressionOfDeclaration(varDecl, param, dependencies_vec, sub_indices_vec)
            paramStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

        if not domain and varDecl != None:
            if varDecl.getIndexingExpression() != None:
                domain = varDecl.getIndexingExpression().generateCode(self)
                paramStr += "{" + domain + "}"

        _types = self._removeTypesThatAreNotDeclarable(_types)
        modifiers = self._getModifiers(_types)

        if len(modifiers) > 0:
            _type = modifiers[0].getName()

            if _type.strip() != "":
                paramStr += " " + _type
        else:
            
            _types = self._getTypes(_types)
            

            if len(_types) > 0:
                _type = _types[0].getName()
                _type = _type if _type != Constants.BINARY_0_1 else Constants.BINARY
                _type = _type if not _type.startswith(Constants.REALSET) else _type[8:]

                if _type.strip() != "":
                    paramStr += " " + _type

        if varDecl != None:
            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute.generateCode(self), ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ",".join(map(lambda el: "in " + el, ins_vec))

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
                self.genValueAssigned.add(GenObj(param))

        paramStr += ";\n\n"

        return paramStr

    def _declareSet(self, _genSet):
        setStr = ""

        setStr += "set " + _genSet.getName()
        domain = None
        dimen = None

        varDecl = self.genDeclarations.get(_genSet.getName())

        domain, domains_vec, dependencies_vec, sub_indices_vec = self._getSubIndicesDomainsAndDependencies(_genSet.getName())
        _types, dim, minVal, maxVal = self._getProperties(_genSet.getName())

        if domain and domain.strip() != "":
            logical = self._getLogicalExpressionOfDeclaration(varDecl, _genSet.getName(), dependencies_vec, sub_indices_vec)
            setStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

        if not domain and varDecl != None:
            if varDecl.getIndexingExpression() != None:
                domain = varDecl.getIndexingExpression().generateCode(self)
                setStr += "{" + domain + "}"

        if dim != None and dim > 1:
            setStr += " dimen " + str(dim)

        if varDecl != None:
            subsets = varDecl.getWithin()
            if subsets != None and len(subsets) > 0:
                setStr += ", " + ",".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), subsets))

            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute.generateCode(self), ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ",".join(map(lambda el: "in " + el, ins_vec))

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

    def _declareDataParam(self, _genParameter):
        res = ""

        if not self.genValueAssigned.has(_genParameter.getName()):
            value = ""
            
            if len(self.identifiers[_genParameter.getName()]["sub_indices"]) == 0:
                if _genParameter.getIsSymbolic():
                    value += " ''"
                else:
                    value += " 0"

            res += "param " + _genParameter.getName() + " :=" + value + ";\n\n"

        return res

    def _declareDataSet(self, _genSet):
        res = ""

        if not self.genValueAssigned.has(_genSet.getName()):
            sub_indices = self.identifiers[_genSet.getName()]["sub_indices"]
            if len(sub_indices) > 0:
                dimenIdx = "[" + ",".join(["0"] * len(sub_indices)) + "]"
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

        self.init()
        graph = self._generateGraph()
        self.topological_order = sort_topologically_stackless(graph)

        res = ""

        setsAndParams = self._declareSetsAndParams()
        if setsAndParams != "":
            res += setsAndParams

        identifiers = self._declareVars()
        if identifiers != "":
            if res != "":
                res += "\n"

            res += identifiers

        return res
    
    def _posModel(self):
        res = "\nsolve;\n\n\n"
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

        res = preModel + node.objectives.generateCode(self) + "\n\n"

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
        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = ", ".join(indexing)

        if node.logicalExpression:
            res += " : " + node.logicalExpression.generateCode(self)

        return res
    
    # Entry Indexing Expression
    def generateCode_EntryIndexingExpressionWithSet(self, node):
        if isinstance(node.identifier, ValueList):
            values = filter(self.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                return ", ".join(map(lambda var: var.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self), values))
        else:
            if self.notInTypesThatAreNotDeclarable(node.identifier):
                return node.identifier.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)

        return ""

    def generateCode_EntryIndexingExpressionCmp(self, node):
        return node.identifier.generateCode(self) + " " + node.op + " " + node.numericExpression.generateCode(self)

    def generateCode_EntryIndexingExpressionEq(self, node):
        if node.hasSup:
            return node.identifier.generateCode(self) + " in " + Utils._getInt(node.value.generateCode(self)) # completed in generateCode_IteratedNumericExpression
        else:
            return node.identifier.generateCode(self) + " in " + node.value.generateCode(self)

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
        if isinstance(node.identifier, ValueList):
            values = filter(self.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                return ", ".join(map(lambda var: var.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self), values))
        else:
            if self.notInTypesThatAreNotDeclarable(node.identifier):
                return node.identifier.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)

        return ""
        '''
        if node.isBinary or node.isInteger or node.isNatural or node.isReal or node.isSymbolic or \
            node.isLogical or node.isDeclaredAsVar or node.isDeclaredAsParam or node.isDeclaredAsSet or \
            isinstance(node.identifier, str):
            return ""
        
        return node.identifier.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)
        '''

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
        if not isinstance(node.value, str):
            return node.value.generateCode(self)
        else:
            return node.value

    def generateCode_SetExpressionWithIndices(self, node):
        var_gen = ""
        if not isinstance(node.identifier, str):
            var_gen = node.identifier.generateCode(self)
        else:
            var_gen = node.identifier

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

    # Identifier List
    def generateCode_IdentifierList(self, node):
        return ",".join(map(self._getCodeValue, node.identifiers))

    # Tuple
    def generateCode_Tuple(self, node):
        return "(" + ",".join(map(self._getCodeValue, node.values)) + ")"

    # Tuple List
    def generateCode_TupleList(self, node):
        return ",".join(map(self._getCodeValue, node.values))

    # Value
    def generateCode_Value(self, node):
        return node.value.generateCode(self)

    # Identifier
    def generateCode_Identifier(self, node):
        if isinstance(node.sub_indices, str):
            return ""

        if len(node.sub_indices) > 0:
            if isinstance(node.sub_indices, list):
                res = node.identifier.generateCode(self) + "[" + ",".join(map(self._getCodeID, node.sub_indices)) + "]"
            else:
                res = node.identifier.generateCode(self) + "[" + self._getCodeID(node.sub_indices) + "]"
        
        else:
            res = node.identifier.generateCode(self)
        
        return res

    # Number
    def generateCode_Number(self, node):
        return node.number

    # ID
    def generateCode_ID(self, node):
        return node.value

    # String
    def generateCode_String(self, node):
        return node.string
