from Utils import *
from ValueList import *
from Tuple import *
from Range import *
from Objectives import *
from Constraints import *
from SetExpression import *
from NodeExpression import *
from ArcExpression import *
from EntryIndexingExpression import *
from SymbolicExpression import *
from TopologicalSort import *
from Constants import *
from SymbolTables import *

from GenSets import *
from GenVariables import *
from GenParameters import *
from GenDeclarations import *
from GenBelongsToList import *
from GenBelongsTo import *

from IntegerSet import *
from RealSet import *
from BinarySet import *
from SymbolicSet import *
from LogicalSet import *
from OrderedSet import *
from CircularSet import *
from ParameterSet import *
from VariableSet import *
from SetSet import *

class CodeGenerator:
    """ Visitor in the Visitor Pattern """
    
    def __init__(self):
        self.genSets = GenSets()
        self.genVariables = GenVariables()
        self.genParameters = GenParameters()
        self.genDeclarations = GenDeclarations()
        self.genBelongsToList = GenBelongsToList()
        self.genValueAssigned = GenList()
        self.genArcObj = GenList()
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
                    domain, domain_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                    self.identifiers[var.getName()] = {"types": _types,
                                                       "dim": dim,
                                                       "minVal": minVal,
                                                       "maxVal": maxVal,
                                                       "domain": domain, 
                                                       "domain_list": domain_list, 
                                                       "dependencies": dependencies, 
                                                       "sub_indices": sub_indices, 
                                                       "statement": stmtIndex}

        if len(self.genParameters) > 0:
            for var in self.genParameters.getAll():
                domain, domain_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domain_list": domain_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices, 
                                                   "statement": stmtIndex}

        if len(self.genSets) > 0:
            for var in self.genSets.getAll():
                domain, domain_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domain_list": domain_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices, 
                                                   "statement": stmtIndex}

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

    def _getLogicalExpressionOfDeclaration(self, declaration, varName, dependencies, sub_indices, stmtIndex):
        if declaration == None or declaration.getIndexingExpression() == None:
            return None

        indexingExpression = declaration.getIndexingExpression()
        if not stmtIndex in indexingExpression:
            return None

        logicalExpression = indexingExpression[stmtIndex].logicalExpression

        if not logicalExpression:
            return None

        logicalExpressionDependencies = set(logicalExpression.getDependencies(self))

        if varName in logicalExpressionDependencies:
            return logicalExpression.generateCode(self)

        if sub_indices and len(logicalExpressionDependencies.intersection(sub_indices)) > 0:
            return logicalExpression.generateCode(self)

        if dependencies and len(logicalExpressionDependencies.intersection(dependencies)) > 0:
            return logicalExpression.generateCode(self)

        return None

    def _getSubIndicesDomainsAndDependencies(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["domain"], res["domain_list"], res["dependencies"], res["sub_indices"], res["statement"]

        return None, [], [], [], None

    def _getProperties(self, var):
        
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["types"], res["dim"], res["minVal"], res["maxVal"]

        return None, [], [], []

    def _getSetAttribute(self, attribute):
        if isinstance(attribute, SetExpressionWithValue):
            return attribute.value
        else:
            return attribute

    def _isFromZeroToN(self, values):
        i = 0
        for idx in values:
            if idx != i:
                return False

            i += 1

        return True

    def _hasEqualIndices(self, minVal, maxVal):
        minValIndices = sorted(minVal.keys())
        maxValIndices = sorted(maxVal.keys())

        return minValIndices == maxValIndices

    def _hasAllIndices(self, minVal, maxVal):
        minValIndices = sorted(minVal.keys())
        maxValIndices = sorted(maxVal.keys())

        if minValIndices != maxValIndices:
            return False

        if not self._isFromZeroToN(minValIndices):
            return False

        if not self._isFromZeroToN(maxValIndices):
            return False

        return True

    def _zipMinMaxVals(self, minVal, maxVal):
        minMaxVals = {}

        for idx in minVal:
            if idx in maxVal:
                minMaxVals[idx] = str(minVal[idx])+FROM_TO+str(maxVal[idx])

        return minMaxVals

    def _isIdentifierType(self, obj):
        return isinstance(obj, ParameterSet) or isinstance(obj, SetSet) or isinstance(obj, VariableSet)

    def _isNumberSet(self, obj):
        return isinstance(obj, BinarySet) or isinstance(obj, IntegerSet) or isinstance(obj, RealSet) or (isinstance(obj, SetExpression) and obj.getSymbolName(self).replace(SPACE, EMPTY_STRING) == Constants.BINARY_0_1)

    def _isModifierSet(self, obj):
        return isinstance(obj, SymbolicSet) or isinstance(obj, LogicalSet) or isinstance(obj, OrderedSet) or isinstance(obj, CircularSet)

    def notInTypesThatAreNotDeclarable(self, value):
        if isinstance(value, Tuple):
            return True
        
        value = value.getSymbol()
        
        return not value.isBinary and not value.isInteger and not value.isNatural and not value.isReal and not value.isSymbolic and not \
        value.isLogical and not value.isOrdered and not value.isCircular and not value.isDeclaredAsVar and not value.isDeclaredAsParam and not \
        value.isDeclaredAsSet and not isinstance(value, str)

    def _removeTypesThatAreNotDeclarable(self, _types):
        return filter(lambda el: not self._isIdentifierType(el.getObj()), _types)

    def _removePreDefinedTypes(self, _types):
        return filter(lambda el: not self._isIdentifierType(el) and not self._isNumberSet(el) and not self._isModifierSet(el), _types)

    def _getTypes(self, _types):
        return filter(lambda el: self._isNumberSet(el.getObj()), _types)

    def _getModifiers(self, _types):
        return filter(lambda el: self._isModifierSet(el.getObj()), _types)

    def _domainIdentifierType(self, domain):
        obj = domain.getObj()
        return self._isIdentifierType(obj)

    def _domainIsNumberSet(self, domain):
        obj = domain.getObj()
        return self._isNumberSet(obj)

    def _domainIsModifierSet(self, domain):
        obj = domain.getObj()
        return self._isModifierSet(obj)

    def _domainIsInvalid(self, domain):
        return self._domainIdentifierType(domain) or self._domainIsNumberSet(domain) or self._domainIsModifierSet(domain)

    def _getNumber(self, numericExpression):
        if isinstance(numericExpression, Number):
            return numericExpression

        if not isinstance(numericExpression, ValuedNumericExpression):
            return None

        value = numericExpression.getValue()
        if isinstance(value, Number):
            return value

        return None

    def _mountValueByIndex(self, indicesPosition, value):
        valueDict = {}

        if isinstance(indicesPosition, list):
            for idx in indicesPosition:
                valueDict[idx] = value
        else:
            valueDict[indicesPosition] = value

        return valueDict

    def _isKeysInDictionary(self, keys, dictionary):
        if isinstance(keys, list):
            for idx in keys:
                if not idx in dictionary:
                    return False

            return True

        else:
            return keys in dictionary

    def _isRangeThatCanBeImproved(self, obj, indicesPosition, minVal, maxVal):
        asc = True
        rangeObj = {}

        if not isinstance(obj, Range):
            return False, asc, rangeObj, minVal, maxVal

        rangeInit = obj.getRangeInit()
        rangeEnd  = obj.getRangeEnd()

        numberInit = self._getNumber(rangeInit)
        numberEnd  = self._getNumber(rangeEnd)

        if not isinstance(numberInit, Number) and not isinstance(numberEnd, Number):
            return False, asc, rangeObj, minVal, maxVal

        if isinstance(numberInit, Number) and isinstance(numberEnd, Number):
            numberInit = int(numberInit.getNumber())
            numberEnd  = int(numberEnd.getNumber())

            minV = numberInit if numberInit < numberEnd  else numberEnd
            maxV = numberEnd  if numberEnd  > numberInit else numberInit

            minValAux = self._mountValueByIndex(indicesPosition, minV)
            minVal = self._setMinVal(minVal, minValAux)

            maxValAux = self._mountValueByIndex(indicesPosition, maxV)
            maxVal = self._setMaxVal(maxVal, maxValAux)

            return True, asc, rangeObj, minVal, maxVal

        by = obj.getBy()

        if by != None:
            numberBy = self._getNumber(by)
            if numberBy == None:
                return False, asc, rangeObj, minVal, maxVal
                
            elif int(numberBy.getNumber()) < 0:
                asc = False

        if isinstance(numberInit, Number):
            numberInit = int(numberInit.getNumber())

            minValAux = self._mountValueByIndex(indicesPosition, numberInit)
            minVal = self._setMinVal(minVal, minValAux)

            maxValAux = self._mountValueByIndex(indicesPosition, numberInit)
            maxVal = self._setMaxVal(maxVal, maxValAux)

        else:

            if not asc:
                rangeObj[1] = obj.getRangeInit()
            else:
                rangeObj[0] = obj.getRangeInit()

        if isinstance(numberEnd, Number):
            numberEnd = int(numberEnd.getNumber())

            minValAux = self._mountValueByIndex(indicesPosition, numberEnd)
            minVal = self._setMinVal(minVal, minValAux)

            maxValAux = self._mountValueByIndex(indicesPosition, numberEnd)
            maxVal = self._setMaxVal(maxVal, maxValAux)

        else:

            if not asc:
                rangeObj[0] = obj.getRangeEnd()
            else:
                rangeObj[1] = obj.getRangeEnd()

        return True, asc, rangeObj, minVal, maxVal

    def _getItemDomain(self, domains, totalIndices):
        size = len(domains)
        if size == 0:
            return None, None, None, None

        while size > 0:
            size -= 1
            domain = domains[size]

            if self._domainIsInvalid(domain):
                continue

            dependencies = list(domain.getDependencies())

            if domain.getName() in dependencies:
                dependencies.remove(domain.getName())

            if len(dependencies) > 0:
                if not set(dependencies).issubset(set(totalIndices+self.parameters_and_sets)):

                    break

            deps = set(domain.getDependencies())
            deps.discard(set(totalIndices))

            return domain.getOp(), domain.getName(), domain.getObj(), list(deps)

        return None, None, None, None

    def _getDomainSubIndices(self, table, selectedIndices, totalIndices, indicesPosition, minVal, maxVal, isDeclaration = False):
        if not isinstance(selectedIndices, str):
            selectedIndices = COMMA.join(selectedIndices)

        rangeObjAux = {}
        domainAux = None
        opAux = None
        depsAux = None

        while table != None:
            value = table.lookup(selectedIndices)

            if value != None:
                op, domain, domainObj, deps = self._getItemDomain(value.getProperties().getDomains(), totalIndices)
                
                if domain != None:

                    if not isDeclaration:
                        isRangeThatCanBeImproved, asc, rangeObj, minVal, maxVal = self._isRangeThatCanBeImproved(domainObj, indicesPosition, minVal, maxVal)
                        
                        if isRangeThatCanBeImproved:
                            opAux = op
                            depsAux = deps
                            domainAux = domain
                            
                            if not rangeObjAux and rangeObj:
                                rangeObjAux = rangeObj

                            table = table.getParent()
                            continue

                        posBy = domain.find(BY) # if a range is inferred as the domain, the by clause is removed

                        if posBy > 0:
                            domain = domain[0:posBy].strip()

                    return op, domain, domainObj, deps, minVal, maxVal

            table = table.getParent()

        if domainAux != None:
            posIn = domainAux.find(SPACE+IN+SPACE)

            if posIn > 0:
                domain = domainAux[0:posIn+4]
            else:
                domain = EMPTY_STRING

            domains = []

            if rangeObjAux:
                
                if 0 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, maxVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(rangeObjAux[0].generateCode(self) + FROM_TO + str(maxVal[idx]))

                        else:
                            domains.append(rangeObjAux[0].generateCode(self) + FROM_TO + str(maxVal[indicesPosition]))

                elif 1 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, minVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(str(minVal[idx]) + FROM_TO + rangeObjAux[1].generateCode(self))

                        else:
                            domains.append(str(minVal[indicesPosition]) + FROM_TO + rangeObjAux[1].generateCode(self))

            else:

                if not self._isKeysInDictionary(indicesPosition, minVal) or not self._isKeysInDictionary(indicesPosition, maxVal):
                    domains = []

                else:

                    if isinstance(indicesPosition, list):
                        for idx in indicesPosition:
                            domains.append(str(minVal[idx]) + FROM_TO + str(maxVal[idx]))

                    else:
                        domains.append(str(minVal[indicesPosition]) + FROM_TO + str(maxVal[indicesPosition]))

            if len(domains) > 1:
                domain += BEGIN_SET+(COMMA+SPACE).join(domains)+END_SET

            elif len(domains) > 0:
                domain += domains[0]

            if len(domains) > 0:
                return opAux, domain, None, depsAux, minVal, maxVal

        return None, None, None, None, minVal, maxVal

    def _getSubIndicesDomainsByTables(self, name, tables, minVal, maxVal, isDeclaration = False, domainsAlreadyComputed = None, skip_outermost_scope = False):

        domain = EMPTY_STRING
        domains_ret = []
        dependencies_ret = []
        sub_indices_ret = []
        max_length_domain = 0

        countAlreadyComputed = {}
        dependenciesAlreadyComputed = {}
        subIndicesAlreadyComputed = {}

        if not domainsAlreadyComputed:
            domainsAlreadyComputed = {}

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

                domain = EMPTY_STRING
                domains = {}
                dependencies = {}
                count = {}
                
                for _subIndices in sub_indices_list:

                    max_length_domain = max(max_length_domain, len(_subIndices))

                    totalIndices = list(_subIndices)
                    idx = 0
                    totalSubIndices = len(_subIndices)
                    indices = range(totalSubIndices)
                    indicesBkp = list(indices)
                    _subIndicesRemaining = list(_subIndices)

                    while idx < totalSubIndices:
                        _combIndices = _subIndices[idx:]
                        _indicesPos = indicesBkp[idx:]
                        
                        if len(_combIndices) <= 1:
                            idx += 1
                            continue

                        op, _tuple, _tupleObj, deps, minVal, maxVal = self._getDomainSubIndices(table, _combIndices, totalIndices, _indicesPos, minVal, maxVal, isDeclaration)
                        while _tuple == None and len(_combIndices) > 0:
                            _combIndices = _combIndices[:-1];
                            _indicesPos = _indicesPos[:-1];
                            
                            if len(_combIndices) <= 1:
                                break

                            op, _tuple, _tupleObj, deps, minVal, maxVal = self._getDomainSubIndices(table, _combIndices, totalIndices, _indicesPos, minVal, maxVal, isDeclaration)
                            
                        if _tuple != None:
                            domains[idx] = BEGIN_ARGUMENT_LIST + COMMA.join(_combIndices) + END_ARGUMENT_LIST+SPACE + op + SPACE + _tuple
                            dependencies[idx] = deps
                            count[idx] = len(_combIndices)
                            
                            for i in range(idx, idx+len(_combIndices)):
                                indices.remove(i)

                            idx += len(_combIndices)

                            for _comb in _combIndices:
                                _subIndicesRemaining.remove(_comb)

                        else:
                            idx += 1
                        
                    if len(indices) > 0:
                        indices = sorted(indices)

                        subIdxDomains = [self._getDomainSubIndices(table, _subIndicesRemaining[i], totalIndices, indices[i], minVal, maxVal, isDeclaration) for i in range(len(_subIndicesRemaining))]
                        subIdxDomainsRemaining = []

                        varNameSubIndices = []
                        for i in range(len(subIdxDomains)):
                            ind = indices[i]
                            minVal = subIdxDomains[i][4]
                            maxVal = subIdxDomains[i][5]

                            if subIdxDomains[i][1] != None:
                                domains[ind] = (_subIndicesRemaining[i] + SPACE + subIdxDomains[i][0] + SPACE if not _subIndicesRemaining[i] in varNameSubIndices else EMPTY_STRING) + subIdxDomains[i][1]
                                dependencies[ind] = subIdxDomains[i][3]
                                count[ind] = 1
                                varNameSubIndices.append(_subIndicesRemaining[i])

                            else:
                                subIdxDomainsRemaining.append(ind)

                    for idx in domains:
                        if not idx in domainsAlreadyComputed or FROM_TO in domainsAlreadyComputed[idx]:
                            domainsAlreadyComputed[idx]      = domains[idx]
                            dependenciesAlreadyComputed[idx] = dependencies[idx]
                            subIndicesAlreadyComputed[idx]   = _subIndices[idx]
                            countAlreadyComputed[idx]   = count[idx]
                            
                table = table.getParent()
        
        totalCountAlreadyComputed = 0
        for idx in countAlreadyComputed:
            totalCountAlreadyComputed += countAlreadyComputed[idx]

        if totalCountAlreadyComputed == max_length_domain:
            domains_str = []
            domains_ret = []
            dependencies_ret = []
            sub_indices_ret = []

            for key in sorted(domainsAlreadyComputed.iterkeys()):
                if domainsAlreadyComputed[key] != None:
                    domains_str.append(domainsAlreadyComputed[key])
                    domains_ret.append(domainsAlreadyComputed[key])

                    if key in dependenciesAlreadyComputed:
                        if isinstance(dependenciesAlreadyComputed[key], list):
                            for dep in dependenciesAlreadyComputed[key]:
                                dependencies_ret.append(dep)

                        else:
                            dependencies_ret.append(dependenciesAlreadyComputed[key])

                    if key in subIndicesAlreadyComputed:
                        if isinstance(subIndicesAlreadyComputed[key], list):
                            for dep in subIndicesAlreadyComputed[key]:
                                sub_indices_ret.append(dep)

                        else:
                            sub_indices_ret.append(subIndicesAlreadyComputed[key])

            domain += (COMMA+SPACE).join(domains_str)

        return domain, domains_ret, list(set(dependencies_ret)), sub_indices_ret, minVal, maxVal

    def _getSubIndicesDomainsByStatements(self, name, statements, minVal, maxVal, isDeclaration = False, domainsAlreadyComputed = None):
        domain = ""
        domains = []
        dependencies = []
        sub_indices = []
        stmtIndex = None
        currStmt = None
        
        for stmt in sorted(statements, reverse=True):
            currStmt = stmt

            scopes = self.symbolTables.getFirstScopeByKey(name, stmt)
            domain, domains, dependencies, sub_indices, minVal, maxVal = self._getSubIndicesDomainsByTables(name, scopes, minVal, maxVal, isDeclaration, domainsAlreadyComputed)

            if domain != EMPTY_STRING and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
                stmtIndex = stmt
                break
            
            leafs = self.symbolTables.getLeafs(stmt)
            domain, domains, dependencies, sub_indices, minVal, maxVal = self._getSubIndicesDomainsByTables(name, leafs, minVal, maxVal, isDeclaration, domainsAlreadyComputed, True)

            if domain != EMPTY_STRING and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
                stmtIndex = stmt
                break

        if not stmtIndex:
            stmtIndex = currStmt

        return domain, domains, dependencies, sub_indices, stmtIndex, minVal, maxVal

    def _getSubIndicesDomains(self, identifier):
        _types, dim, minVal, maxVal = self._getDomain(identifier)

        name = identifier.getName()
        declarations = self.symbolTables.getDeclarationsWhereKeyIsDefined(name)
        domain, domains, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, declarations, minVal, maxVal, True)

        if domain == EMPTY_STRING:
            statements = self.symbolTables.getStatementsByKey(name)
            domain, domains, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, statements, minVal, maxVal, False)

        if domain == EMPTY_STRING:
            if minVal and maxVal and self._hasEqualIndices(minVal, maxVal):
                minMaxVals = self._zipMinMaxVals(minVal, maxVal)
                domain, domains, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, declarations, minVal, maxVal, True, minMaxVals)

                if domain == EMPTY_STRING or domains == minMaxVals.values():
                    statements = self.symbolTables.getStatementsByKey(name)
                    domain, domains, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, statements, minVal, maxVal, False, minMaxVals)

        return domain, domains, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal

    def _setMinVal(self, minVal, minValAux):
        if minVal == None:
            minVal = {}

        if minValAux == None or len(minValAux) == 0:
            return minVal
            
        for idx in minValAux:
            if not idx in minVal or minValAux[idx] < minVal[idx]:
                minVal[idx] = minValAux[idx]

        return minVal

    def _setMaxVal(self, maxVal, maxValAux):
        if maxVal == None:
            maxVal = {}
            
        if maxValAux == None or len(maxValAux) == 0:
            return maxVal
        
        for idx in maxValAux:
            if not idx in maxVal or maxValAux[idx] > maxVal[idx]:
                maxVal[idx] = maxValAux[idx]

        return maxVal

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
                domains.reverse()

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

                minVal = self._setMinVal(minVal, prop.getMinVal())
                maxVal = self._setMaxVal(maxVal, prop.getMaxVal())

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
        
    def _addDependencies(self, value, stmtIndex, dependencies):
        names = value.getDependencies(self)

        if names != None and len(names) > 0:
            for name in names:
                if not self.genBelongsToList.has(GenBelongsTo(name, stmtIndex)):
                    dependencies.append(name)

    def _getDependencies(self, identifier):
        dependencies = []

        decl = self.genDeclarations.get(identifier.getName())
        if decl != None:
            value = decl.getValue()
            if value != None:
                self._addDependencies(value.attribute, decl.getStmtIndex(), dependencies)

            value = decl.getDefault()
            if value != None:
                self._addDependencies(value.attribute, decl.getStmtIndex(), dependencies)

            ins = decl.getIn()
            if ins != None and len(ins) > 0:
                for pSet in ins:
                    self._addDependencies(pSet.attribute, decl.getStmtIndex(), dependencies)

            withins = decl.getWithin()
            if withins != None and len(withins) > 0:
                for pSet in withins:
                    self._addDependencies(pSet.attribute, decl.getStmtIndex(), dependencies)

            relations = decl.getRelations()
            if relations != None and len(relations) > 0:
                for pRel in relations:
                    self._addDependencies(pRel.attribute, decl.getStmtIndex(), dependencies)

            idxsExpression = decl.getIndexingExpression()
            _subIndices = decl.getSubIndices()
            for stmtIndex in idxsExpression:
                if idxsExpression[stmtIndex] and stmtIndex in _subIndices and _subIndices[stmtIndex]:
                    idxExpression = idxsExpression[stmtIndex]

                    self._addDependencies(idxExpression, stmtIndex, dependencies)

        return dependencies

    def _checkAddDependence(self, graph, name, dep):
        return dep != name and not dep in graph[name] and dep in self.parameters_and_sets

    def _generateGraphAux(self, graph, genObj):
        if len(genObj) > 0:
            for identifier in genObj.getAll():
                
                name = identifier.getName()
                if not name in graph:
                    graph[name] = []
                
                dependencies = self._getDependencies(identifier)

                if len(dependencies) > 0:
                    for dep in dependencies:
                        if self._checkAddDependence(graph, name, dep):
                            graph[name].append(dep)

                _domain, domains_vec, dependencies_vec, sub_indices, stmtIndex = self._getSubIndicesDomainsAndDependencies(identifier.getName())

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


    def _getValueFromNumericExpression(self, expr):
        if isinstance(expr, ValuedNumericExpression):
            return expr.value

        return expr

    # Get the AMPL code for a value
    def _getCodeValue(self, value):
        val = value.generateCode(self)
        return val

    # Get the AMPL code for a given sub-indice
    def _getCodeID(self, id_):
        if isinstance(id_, ValuedNumericExpression):
            if isinstance(id_.value, Identifier):
                id_.value.setIsSubIndice(True)

        elif isinstance(id_, Identifier):
            id_.setIsSubIndice(True)

        val = id_.generateCode(self)

        return val

    # Get the AMPL code for a given entry
    def _getCodeEntry(self, entry):
        return entry.generateCode(self)

    # Get the AMPL code for a given entry
    def _getCodeEntryByKey(self, entry):
        for key in entry:
            return key, entry[key].generateCode(self)

    # Get the AMPL code for a given objective
    def _getCodeObjective(self, objective):
        self.objectiveNumber += 1
        return objective.generateCode(self)

    # Get the AMPL code for a given constraint
    def _getCodeConstraint(self, constraint):
        if isinstance(constraint, Constraint):
            constraintStmt = constraint.generateCode(self)

            if constraintStmt and constraintStmt.strip():
                constraintStmt = constraintStmt.strip()

                self.constraintNumber += 1
                return SUBJECT_TO+SPACE+"C" + str(self.constraintNumber) + SPACE + constraintStmt

        elif isinstance(constraint, NodeExpression):
            nodeStmt = constraint.generateCode(self)

            if nodeStmt and nodeStmt.strip():
                nodeStmt = nodeStmt.strip()
                return NODE+SPACE+nodeStmt

        elif isinstance(constraint, ArcExpression):
            arcStmt = constraint.generateCode(self)

            if arcStmt and arcStmt.strip():
                arcStmt = arcStmt.strip()
                return ARC+SPACE+arcStmt
                
        elif isinstance(constraint, Objective):
            return self._getCodeObjective(constraint)

        return EMPTY_STRING

    def _getIndexingExpressionFromDeclarations(self, decl):
        idxsExpression = decl.getIndexingExpression()
        _subIndices = decl.getSubIndices()

        for stmtIndex in sorted(idxsExpression, reverse=True):
            if idxsExpression[stmtIndex] and stmtIndex in _subIndices and _subIndices[stmtIndex]:
                idxExpression = idxsExpression[stmtIndex]

                return idxExpression

        return None

    def _processDomain(self, name, domain, minVal, maxVal, declaration, dependencies_vec, sub_indices_vec, stmtIndex):

        result = EMPTY_STRING

        if domain != None and domain.strip() != EMPTY_STRING:
            logical = self._getLogicalExpressionOfDeclaration(declaration, name, dependencies_vec, sub_indices_vec, stmtIndex)
            result += BEGIN_SET + domain + (EMPTY_STRING if logical == None else SPACE+SUCH_THAT+SPACE + logical) + END_SET

        elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0:
            if self._hasAllIndices(minVal, maxVal):
                domainMinMax = []
                for i in range(len(minVal)):
                    domainMinMax.append(str(minVal[i])+FROM_TO+str(maxVal[i]))

                domain = (COMMA+SPACE).join(domainMinMax)
                result += BEGIN_SET+domain+END_SET

        if not domain and declaration != None:
            idxExpression = self._getIndexingExpressionFromDeclarations(declaration)
            if idxExpression:
                domain = idxExpression.generateCode(self)
                result += BEGIN_SET + domain + END_SET

        return result, domain

    def _processDeclaration(self, name, declaration, isSet = False, isVariable = False):

        result = EMPTY_STRING
        checkValue = True

        if isSet:
            subsets = declaration.getWithin()
            if subsets != None and len(subsets) > 0:
                result += COMMA+SPACE + (COMMA+SPACE).join(map(lambda el: el.op + SPACE + el.attribute.generateCode(self), subsets))

            dimen = declaration.getDimen()
            if dimen != None:
                result += COMMA+SPACE+DIMENSION+SPACE+dimen.attribute.generateCode(self)

        ins_vec = declaration.getIn()
        ins_vec = self._removePreDefinedTypes(map(lambda el: self._getSetAttribute(el.attribute), ins_vec))
        if ins_vec != None and len(ins_vec) > 0:
            ins = (COMMA+SPACE).join(map(lambda el: IN+SPACE + el.generateCode(self), ins_vec))

            if ins != EMPTY_STRING:
                result += COMMA+SPACE + ins

        if isVariable:
            attr = declaration.getRelationEqualTo()
            if attr != None:
                result += COMMA+SPACE+EQUAL+SPACE + attr.attribute.generateCode(self)
                checkValue = False

        if checkValue:
            if declaration.getValue() != None:
                value = COMMA+SPACE+ASSIGN+SPACE + declaration.getValue().attribute.generateCode(self)
                result += value
                self.genValueAssigned.add(GenObj(name))

            if declaration.getDefault() != None:
                default = COMMA+SPACE+DEFAULT+SPACE + declaration.getDefault().attribute.generateCode(self)
                result += default

            if not isSet:
                relations = declaration.getRelations()
                if relations != None and len(relations) > 0:
                    result += COMMA+SPACE + (COMMA+SPACE).join(map(lambda el: el.op + SPACE + el.attribute.generateCode(self), relations))

        return result

    def _processType(self, _types, isSet = False, isVariable = False):
        result = EMPTY_STRING
        checkTypes = not isSet

        _types = self._removeTypesThatAreNotDeclarable(_types)

        if not isVariable:
            modifiers = self._getModifiers(_types)

            if len(modifiers) > 0:
                _type = modifiers[0].getName()

                if _type.strip() != EMPTY_STRING:
                    result += SPACE + _type
                    checkTypes = False

        if checkTypes:
            _types = self._getTypes(_types)

            if len(_types) > 0:
                _type = _types[0].getName()
                _type = _type if _type != Constants.BINARY_0_1 else Constants.BINARY
                _type = _type if not _type.startswith(Constants.REALSET) else _type[8:]

                if _type.strip() != EMPTY_STRING:
                    result += SPACE + _type

        return result

    def _processObject(self, genObj, objType, isSet, isVariable):

        domain = None
        name = genObj.getName()
        declaration = self.genDeclarations.get(name)

        result = EMPTY_STRING
        result += objType+SPACE+name
        
        domain, domains_vec, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(name)
        _types, dim, minVal, maxVal = self._getProperties(name)
        
        domainStr, domain = self._processDomain(name, domain, minVal, maxVal, declaration, dependencies_vec, sub_indices_vec, stmtIndex)
        result += domainStr

        if isSet and dim != None and dim > 1:
            result += SPACE+DIMENSION+SPACE+str(dim)

        result += self._processType(_types, isSet, isVariable)

        if declaration != None:
            result += self._processDeclaration(name, declaration, isSet, isVariable)

        result += END_STATEMENT+BREAKLINE+BREAKLINE

        return result

    def _declareVars(self):
        """
        Generate the AMPL code for the declaration of identifiers
        """

        result = EMPTY_STRING
        if len(self.genVariables) > 0:
            
            graphVar = {}
            
            self._generateGraphAux(graphVar, self.genVariables)
            topological_order_var = sort_topologically_stackless(graphVar)
            
            for var in topological_order_var:

                if not self.genParameters.has(var) and not self.genSets.has(var):
                    var = self.genVariables.get(var)
                    result += self._declareVar(var)

        return result
        
    def _declareVar(self, var):
        result = self._processObject(var, VARIABLE, False, True)
        return result
        
    def _declareParam(self, _genParameter):

        if self.genArcObj.has(_genParameter.getName()):
            return ""

        result = self._processObject(_genParameter, PARAMETER, False, False)
        return result
        
    def _declareSet(self, _genSet):
        result = self._processObject(_genSet, SET, True, False)
        return result
        
    def _declareSetsAndParams(self):

        paramSetStr = EMPTY_STRING
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
        res = EMPTY_STRING

        if not self.genValueAssigned.has(_genParameter.getName()):
            value = EMPTY_STRING
            
            if len(self.identifiers[_genParameter.getName()]["sub_indices"]) == 0:
                if _genParameter.getIsSymbolic():
                    value += SPACE+"''"
                else:
                    value += SPACE+"0"

            res += PARAMETER+SPACE + _genParameter.getName() + SPACE+ASSIGN + value + END_STATEMENT+BREAKLINE+BREAKLINE

        return res

    def _declareDataSet(self, _genSet):
        res = EMPTY_STRING

        if not self.genValueAssigned.has(_genSet.getName()):
            sub_indices = self.identifiers[_genSet.getName()]["sub_indices"]
            if len(sub_indices) > 0:
                dimenIdx = BEGIN_ARRAY + COMMA.join(["0"] * len(sub_indices)) + END_ARRAY
            else:
                dimenIdx = EMPTY_STRING

            res += SET+SPACE + _genSet.getName() + dimenIdx + SPACE+ASSIGN+END_STATEMENT+BREAKLINE+BREAKLINE

        return res

    def _declareDataSetsAndParams(self):
        res = EMPTY_STRING

        if len(self.topological_order) > 0:
            for paramSetIn in self.topological_order:
                _genObj = self.genParameters.get(paramSetIn)

                if _genObj != None:
                    res += self._declareDataParam(_genObj)
                else:
                    _genObj = self.genSets.get(paramSetIn)

                    if _genObj != None:
                        res += self._declareDataSet(_genObj)

        if res != EMPTY_STRING:
            res = DATA+END_STATEMENT+BREAKLINE+BREAKLINE + res + BREAKLINE

        return res

    def _preModel(self):

        self.init()
        graph = self._generateGraph()
        self.topological_order = sort_topologically_stackless(graph)

        res = EMPTY_STRING

        setsAndParams = self._declareSetsAndParams()
        if setsAndParams != EMPTY_STRING:
            res += setsAndParams

        identifiers = self._declareVars()
        if identifiers != EMPTY_STRING:
            if res != EMPTY_STRING:
                res += BREAKLINE

            res += identifiers

        return res
    
    def _posModel(self):
        res = EMPTY_STRING

        return res

    def generateCode_Main(self, node):
        return node.problem.generateCode(self)

    def generateCode_LinearEquations(self, node):
        preModel = self._preModel()
        if preModel != EMPTY_STRING:
            preModel += BREAKLINE

        return preModel + node.constraints.generateCode(self) + BREAKLINE+BREAKLINE + self._posModel()

    def generateCode_LinearProgram(self, node):
        preModel = self._preModel()
        if preModel != EMPTY_STRING:
            preModel += BREAKLINE

        res = preModel + node.objectives.generateCode(self) + BREAKLINE+BREAKLINE

        if node.constraints:
            res += node.constraints.generateCode(self) + BREAKLINE+BREAKLINE
        
        res += self._posModel()

        return res

    # Objectives
    def generateCode_Objectives(self, node):
        self.totalObjectives = len(node.objectives)
        return (BREAKLINE+BREAKLINE).join(map(self._getCodeObjective, node.objectives))

    # Objective Function
    def generateCode_Objective(self, node):
        """
        Generate the code in AMPL for this Objective
        """
        
        linearExpression = node.linearExpression.generateCode(self)

        if self.genArcObj.has(linearExpression):
            return node.type + SPACE+ linearExpression + END_STATEMENT

        domain_str = EMPTY_STRING
        if node.domain:
            idxExpression = node.domain.generateCode(self)
            if idxExpression:
                domain_str = SPACE+BEGIN_SET + idxExpression + END_SET

        return node.type + SPACE+OBJECTIVE + (str(self.objectiveNumber) if self.objectiveNumber > 1 else EMPTY_STRING)  + domain_str + SUCH_THAT+SPACE + linearExpression + END_STATEMENT

    # Constraints
    def generateCode_Constraints(self, node):
        return (BREAKLINE+BREAKLINE).join(filter(lambda el: el != EMPTY_STRING and el != None, map(self._getCodeConstraint, node.constraints)))

    def generateCode_Constraint(self, node):
        res = EMPTY_STRING
        constraintExpression = node.constraintExpression.generateCode(self)

        if constraintExpression and constraintExpression.strip():
            constraintExpression = constraintExpression.strip()

            if node.indexingExpression:
                idxExpression = node.indexingExpression.generateCode(self)

                if idxExpression.strip() != EMPTY_STRING:
                    res += BEGIN_SET + idxExpression + END_SET+SPACE+SUCH_THAT+BREAKLINE+TAB
                else:
                    res += SPACE+SUCH_THAT+SPACE
            else:
                res += SPACE+SUCH_THAT+SPACE

            res += constraintExpression + END_STATEMENT

        return res

    def generateCode_NodeExpression(self, node):
        res = EMPTY_STRING
        expression = node.netExpression.generateCode(self) + SPACE + node.op + SPACE + node.value.generateCode(self)

        if node.indexingExpression:
            idxExpression = node.indexingExpression.generateCode(self)

            if idxExpression.strip() != EMPTY_STRING:
                res += node.identifier.generateCodeWithoutIndices(self) + SPACE + BEGIN_SET + idxExpression + END_SET+SPACE+SUCH_THAT+BREAKLINE+TAB
            else:
                res += node.identifier.generateCodeWithoutIndices(self) + SPACE+SUCH_THAT+SPACE
        else:
            res += node.identifier.generateCodeWithoutIndices(self) + SPACE+SUCH_THAT+SPACE

        res += expression + END_STATEMENT

        return res

    def generateCode_NetInExpression(self, node):
        return NetInExpression.NETIN

    def generateCode_NetOutExpression(self, node):
        return NetOutExpression.NETOUT

    def generateCode_ArcExpression(self, node):
        res = EMPTY_STRING
        expression = GE + SPACE + node.lowerLimit.generateCode(self) + COMMA + SPACE + LE + SPACE + node.upperLimit.generateCode(self) + COMMA + BREAKLINE+TAB +\
                        FROM + SPACE + node._from.generateCode(self) + COMMA + SPACE + TO + SPACE + node.to.generateCode(self) + \
                        COMMA + SPACE + OBJ + SPACE + node.objName.generateCode(self) + SPACE + node.objValue.generateCode(self)

        if node.indexingExpression:
            idxExpression = node.indexingExpression.generateCode(self)

            if idxExpression.strip() != EMPTY_STRING:
                res += node.identifier.generateCodeWithoutIndices(self) + SPACE + BEGIN_SET + idxExpression + END_SET+SPACE
            else:
                res += node.identifier.generateCodeWithoutIndices(self) + SPACE
        else:
            res += node.identifier.generateCodeWithoutIndices(self) + SPACE

        res += expression + END_STATEMENT

        return res

    def generateCode_ConstraintExpression2(self, node):
        res = node.linearExpression1.generateCode(self) + SPACE + node.op + SPACE + node.linearExpression2.generateCode(self)
        return res

    def generateCode_ConstraintExpression3(self, node):
        res = node.numericExpression1.generateCode(self) + SPACE + node.op + SPACE + node.linearExpression.generateCode(self) + SPACE + node.op + SPACE + node.numericExpression2.generateCode(self)
        return res

    def generateCode_ConditionalConstraintExpression(self, node):
        res = node.logicalExpression.generateCode(self) + SPACE + node.op + SPACE + node.constraintExpression1.generateCode(self)
        
        if node.constraintExpression2:
            res += SPACE+ELSE+SPACE + node.constraintExpression2.generateCode(self)
            
        return res

        
    # Linear Expression
    def generateCode_ValuedLinearExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_LinearExpressionBetweenParenthesis(self, node):
        return BEGIN_ARGUMENT_LIST + node.linearExpression.generateCode(self) + END_ARGUMENT_LIST

    def generateCode_LinearExpressionWithArithmeticOperation(self, node):
        return node.expression1.generateCode(self) + SPACE + node.op + SPACE + node.expression2.generateCode(self)

    def generateCode_MinusLinearExpression(self, node):
        return MINUS + node.linearExpression.generateCode(self)

    def generateCode_IteratedLinearExpression(self, node):

        if node.numericExpression:
            supExpression = self._getValueFromNumericExpression(node.numericExpression)

            if isinstance(supExpression, Identifier) or isinstance(supExpression, Number):
                supExpression = supExpression.generateCode(self)
            else:
                supExpression = BEGIN_ARGUMENT_LIST + supExpression.generateCode(self) + END_ARGUMENT_LIST

            res = SUM + BEGIN_SET + node.indexingExpression.generateCode(self) + FROM_TO+supExpression+END_SET
        else:
            res = SUM + BEGIN_SET + node.indexingExpression.generateCode(self) + END_SET

        res += node.linearExpression.generateCode(self)

        return res

    def generateCode_ConditionalLinearExpression(self, node):
        res = IF+SPACE + node.logicalExpression.generateCode(self)

        if node.linearExpression1:
            res += SPACE+THEN+SPACE + node.linearExpression1.generateCode(self)

            if node.linearExpression2:
                res += SPACE+ELSE+SPACE + node.linearExpression2.generateCode(self)

        return res

    # Numeric Expression
    def generateCode_NumericExpressionWithFunction(self, node):
        if not isinstance(node.function, str):
            function = node.function.generateCode(self)
        else:
            function = node.function

        res = function + BEGIN_ARGUMENT_LIST

        if node.numericExpression1 != None:
            res += node.numericExpression1.generateCode(self)

        if node.numericExpression2 != None:
            res += COMMA+SPACE + node.numericExpression2.generateCode(self)

        res += END_ARGUMENT_LIST

        return res

    def generateCode_FractionalNumericExpression(self, node):
        
        numerator = node.numerator
        if isinstance(node.numerator, ValuedNumericExpression):
            numerator = numerator.value
            
        if not isinstance(numerator, Identifier) and not isinstance(numerator, Number) and not isinstance(numerator, NumericExpressionWithFunction):
            numerator = BEGIN_ARGUMENT_LIST+numerator.generateCode(self)+END_ARGUMENT_LIST
        else:
            numerator = numerator.generateCode(self)
            
        denominator = node.denominator
        if isinstance(denominator, ValuedNumericExpression):
            denominator = denominator.value
            
        if not isinstance(denominator, Identifier) and not isinstance(denominator, Number) and not isinstance(denominator, NumericExpressionWithFunction):
            denominator = BEGIN_ARGUMENT_LIST+denominator.generateCode(self)+END_ARGUMENT_LIST
        else:
            denominator = denominator.generateCode(self)
            
        return numerator+DIV+denominator
        
    def generateCode_ValuedNumericExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_NumericExpressionBetweenParenthesis(self, node):
        return BEGIN_ARGUMENT_LIST + node.numericExpression.generateCode(self) + END_ARGUMENT_LIST

    def generateCode_NumericExpressionWithArithmeticOperation(self, node):
        res = node.numericExpression1.generateCode(self) + SPACE + node.op + SPACE

        if node.op == NumericExpressionWithArithmeticOperation.POW and not (isinstance(node.numericExpression2, ValuedNumericExpression) or isinstance(node.numericExpression2, NumericExpressionBetweenParenthesis)):
            res += BEGIN_ARGUMENT_LIST + node.numericExpression2.generateCode(self) + END_ARGUMENT_LIST
        else:
            res += node.numericExpression2.generateCode(self)

        return res

    def generateCode_MinusNumericExpression(self, node):
        return MINUS + node.numericExpression.generateCode(self)

    def generateCode_IteratedNumericExpression(self, node):
        if node.supNumericExpression:
            
            supExpression = self._getValueFromNumericExpression(node.supNumericExpression)

            if isinstance(supExpression, Identifier) or isinstance(supExpression, Number):
                supExpression = supExpression.generateCode(self)
            else:
                supExpression = BEGIN_ARGUMENT_LIST + supExpression.generateCode(self) + END_ARGUMENT_LIST

            res = str(node.op) + BEGIN_SET + node.indexingExpression.generateCode(self) + FROM_TO+supExpression+END_SET
        else:
            res = str(node.op) + BEGIN_SET + node.indexingExpression.generateCode(self) + END_SET

        res += node.numericExpression.generateCode(self)

        return res

    def generateCode_IteratedNumericExpression2(self, node):
        res = node.op

        if node.numericExpression:
            res += SPACE + node.numericExpression.generateCode(self)

        if node.op == IteratedNumericExpression2.NUMBEROF:
            res += SPACE+IN+SPACE+BEGIN_ARGUMENT_LIST+BEGIN_SET+ node.indexingExpression.generateCode(self) +END_SET+SPACE + node.constraintExpression.generateCode(self) + END_ARGUMENT_LIST

        else:
            res += SPACE+BEGIN_SET+ node.indexingExpression.generateCode(self) +END_SET+SPACE + node.constraintExpression.generateCode(self)

        return res

    def generateCode_ConditionalNumericExpression(self, node):
        res = IF+SPACE + node.logicalExpression.generateCode(self) + SPACE+THEN+SPACE + node.numericExpression1.generateCode(self)

        if node.numericExpression2:
            res += SPACE+ELSE+SPACE + node.numericExpression2.generateCode(self)

        return res
        
    # Symbolic Expression
    def generateCode_SymbolicExpressionWithFunction(self, node):
        res = str(node.function) + BEGIN_ARGUMENT_LIST

        if node.function == SymbolicExpressionWithFunction.SPRINTF:
            res += node.firstExpression.generateCode(self) + COMMA + node.numericExpression1.generateCode(self)

        elif node.function == SymbolicExpressionWithFunction.CTIME:
            if node.firstExpression != None:
                res += node.firstExpression.generateCode(self)

        elif node.function == SymbolicExpressionWithFunction.ALIAS or node.function == SymbolicExpressionWithFunction.CHAR:
            res += node.firstExpression.generateCode(self)

        elif node.function == SymbolicExpressionWithFunction.SUBSTR or node.function == SymbolicExpressionWithFunction.SUB or node.function == SymbolicExpressionWithFunction.GSUB:
            res += node.firstExpression.generateCode(self) + COMMA + node.numericExpression1.generateCode(self)
            if node.numericExpression2 != None:
                res += COMMA + node.numericExpression2.generateCode(self)
                
        elif node.function == SymbolicExpressionWithFunction.TIME2STR:
            res += node.firstExpression.generateCode(self) + COMMA + node.numericExpression1.generateCode(self)

        res += END_ARGUMENT_LIST

        return res

    def generateCode_StringSymbolicExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_SymbolicExpressionBetweenParenthesis(self, node):
        return BEGIN_ARGUMENT_LIST + node.symbolicExpression.generateCode(self) + END_ARGUMENT_LIST

    def generateCode_SymbolicExpressionWithOperation(self, node):
        return node.symbolicExpression1.generateCode(self) + SPACE + node.op + SPACE + node.symbolicExpression2.generateCode(self)

    def generateCode_ConditionalSymbolicExpression(self, node):
        res = IF+SPACE + node.logicalExpression.generateCode(self) + SPACE+THEN+SPACE + node.symbolicExpression1.generateCode(self)

        if node.symbolicExpression2 != None:
            res += SPACE+ELSE+SPACE + node.symbolicExpression2.generateCode(self)

        return res

    # Indexing Expression
    def generateCode_IndexingExpression(self, node):
        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = (COMMA+SPACE).join(indexing)

        if node.logicalExpression:
            res += SPACE+SUCH_THAT+SPACE + node.logicalExpression.generateCode(self)

        return res
    
    # Entry Indexing Expression
    def generateCode_EntryIndexingExpressionWithSet(self, node):
        if isinstance(node.identifier, ValueList):
            values = filter(self.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                return (COMMA+SPACE).join(map(lambda var: var.generateCode(self) + SPACE + node.op + SPACE + node.setExpression.generateCode(self), values))
        else:
            if self.notInTypesThatAreNotDeclarable(node.identifier):
                return node.identifier.generateCode(self) + SPACE + node.op + SPACE + node.setExpression.generateCode(self)

        return EMPTY_STRING

    def generateCode_EntryIndexingExpressionCmp(self, node):
        return node.identifier.generateCode(self) + SPACE + node.op + SPACE + node.numericExpression.generateCode(self)

    def generateCode_EntryIndexingExpressionEq(self, node):
        if node.hasSup:
            return node.identifier.generateCode(self) + SPACE+IN+SPACE + Utils._getInt(node.value.generateCode(self)) # completed in generateCode_IteratedNumericExpression
        else:
            return node.identifier.generateCode(self) + SPACE+IN+SPACE + node.value.generateCode(self)

    # Logical Expression
    def generateCode_LogicalExpression(self, node):
        res = EMPTY_STRING
        first = True

        for i in range(len(node.entriesLogicalExpression)):
            conj, code = self._getCodeEntryByKey(node.entriesLogicalExpression[i])

            if code != 0:
                if first:
                    first = False
                    res += code
                else:
                    res += SPACE + conj + SPACE + code

        return res

    # Entry Logical Expression
    def generateCode_EntryLogicalExpressionRelational(self, node):
        return node.numericExpression1.generateCode(self) + SPACE + node.op + SPACE + node.numericExpression2.generateCode(self)

    def generateCode_EntryLogicalExpressionWithSet(self, node):
        if isinstance(node.identifier, ValueList):
            values = filter(self.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                return (SPACE+AND+SPACE).join(map(lambda var: var.generateCode(self) + SPACE + node.op + SPACE + node.setExpression.generateCode(self), values))
        else:
            if self.notInTypesThatAreNotDeclarable(node.identifier):
                return node.identifier.generateCode(self) + SPACE + node.op + SPACE + node.setExpression.generateCode(self)

        return EMPTY_STRING

    def generateCode_EntryLogicalExpressionWithSetOperation(self, node):
        return node.setExpression1.generateCode(self) + SPACE + node.op + SPACE + node.setExpression2.generateCode(self)

    def generateCode_EntryLogicalExpressionIterated(self, node):
        return node.op + BEGIN_SET + node.indexingExpression.generateCode(self) + END_SET+SPACE +  node.logicalExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionBetweenParenthesis(self, node):
        return BEGIN_ARGUMENT_LIST + node.logicalExpression.generateCode(self) + END_ARGUMENT_LIST

    def generateCode_EntryLogicalExpressionNot(self, node):
        return NOT+SPACE + node.logicalExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionNumericOrSymbolic(self, node):
        return node.numericOrSymbolicExpression.generateCode(self)

    # Set Expression
    def generateCode_SetExpressionWithValue(self, node):
        if not isinstance(node.value, str):
            return node.value.generateCode(self)
        else:
            return node.value

    def generateCode_SetExpressionWithIndices(self, node):
        var_gen = EMPTY_STRING
        if not isinstance(node.identifier, str):
            var_gen = node.identifier.generateCode(self)
        else:
            var_gen = node.identifier

        return  var_gen

    def generateCode_SetExpressionWithOperation(self, node):
        return node.setExpression1.generateCode(self) + SPACE + node.op + SPACE+ node.setExpression2.generateCode(self)

    def generateCode_SetExpressionBetweenBraces(self, node):
        if node.setExpression != None:
            setExpression = node.setExpression.generateCode(self)
        else:
            setExpression = EMPTY_STRING

        return BEGIN_SET + setExpression + END_SET

    def generateCode_SetExpressionBetweenParenthesis(self, node):
        return BEGIN_ARGUMENT_LIST + node.setExpression.generateCode(self) + END_ARGUMENT_LIST

    def generateCode_IteratedSetExpression(self, node):
        res = node.op

        if node.supExpression:
            supExpression = self._getValueFromNumericExpression(node.supExpression)

            if isinstance(supExpression, Identifier) or isinstance(supExpression, Number):
                supExpression = supExpression.generateCode(self)
            else:
                supExpression = BEGIN_ARGUMENT_LIST + supExpression.generateCode(self) + END_ARGUMENT_LIST

            res += SPACE+BEGIN_SET + node.indexingExpression.generateCode(self) + FROM_TO+supExpression+END_SET+SPACE
        else:
            res += SPACE+BEGIN_SET + node.indexingExpression.generateCode(self) + END_SET+SPACE

        res += node.integrand.generateCode(self)

        return res

    def generateCode_ConditionalSetExpression(self, node):
        res = IF+SPACE + node.logicalExpression.generateCode(self) + SPACE+THEN+SPACE + node.setExpression1.generateCode(self)

        if node.setExpression2:
            res += SPACE+ELSE+SPACE + node.setExpression2.generateCode(self)

        else:
            res += SPACE+ELSE+SPACE+EMPTY_SET

        return res

    # Range
    def generateCode_Range(self, node):
        initValue = node.rangeInit.generateCode(self)
        initValue = Utils._getInt(initValue)

        endValue = node.rangeEnd.generateCode(self)
        endValue = Utils._getInt(endValue)

        res = initValue + FROM_TO + endValue
        if node.by != None:
            res += SPACE+BY+SPACE + node.by.generateCode(self)

        return res

    # Value List
    def generateCode_ValueList(self, node):
        return COMMA.join(map(self._getCodeValue, node.values))

    # Identifier List
    def generateCode_IdentifierList(self, node):
        return COMMA.join(map(self._getCodeValue, node.identifiers))

    # Tuple
    def generateCode_Tuple(self, node):
        return BEGIN_ARGUMENT_LIST + COMMA.join(map(self._getCodeValue, node.values)) + END_ARGUMENT_LIST

    # Tuple List
    def generateCode_TupleList(self, node):
        return COMMA.join(map(self._getCodeValue, node.values))

    # Value
    def generateCode_Value(self, node):
        return node.value.generateCode(self)

    # Identifier
    def generateCode_Identifier(self, node):
        if isinstance(node.sub_indices, str):
            return EMPTY_STRING

        if len(node.sub_indices) > 0:
            if isinstance(node.sub_indices, list):
                res = node.identifier.generateCode(self) + BEGIN_ARRAY + COMMA.join(map(self._getCodeID, node.sub_indices)) + END_ARRAY
            else:
                res = node.identifier.generateCode(self) + BEGIN_ARRAY + self._getCodeID(node.sub_indices) + END_ARRAY
        
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

    # IntegerSet
    def generateCode_IntegerSet(self, node):
        res = INTEGER
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = EMPTY_STRING
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += COMMA+SPACE
            else:
                op += SPACE
                
            op += node.firstOp+SPACE
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = EMPTY_STRING
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += COMMA+SPACE
            else:
                op += SPACE
                
            op += node.secondOp+SPACE
            
            res += op + secondBound
            
        return res

    # RealSet
    def generateCode_RealSet(self, node):
        res = EMPTY_STRING
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = EMPTY_STRING
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += COMMA+SPACE
                
            op += node.firstOp+SPACE
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = EMPTY_STRING
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += COMMA+SPACE
                
            op += node.secondOp+SPACE
            
            res += op + secondBound
            
        return res

    # BinarySet
    def generateCode_BinarySet(self, node):
        return BINARY

    # SymbolicSet
    def generateCode_SymbolicSet(self, node):
        return SYMBOLIC

    # LogicalSet
    def generateCode_LogicalSet(self, node):
        return LOGICAL

    # SymbolicSet
    def generateCode_OrderedSet(self, node):
        return ORDERED

    # LogicalSet
    def generateCode_CircularSet(self, node):
        return CIRCULAR

    # ParameterSet
    def generateCode_ParameterSet(self, node):
        return EMPTY_STRING

    # SymbolicSet
    def generateCode_VariableSet(self, node):
        return EMPTY_STRING

    # SetSet
    def generateCode_SetSet(self, node):
        return EMPTY_STRING
