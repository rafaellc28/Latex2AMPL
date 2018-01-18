from Utils import *
from ValueList import *
from Tuple import *
from Range import *
from Objectives import *
from Constraints import *
from SetExpression import *
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
from SymbolicSet import *
from LogicalSet import *
from BinarySet import *
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
                minMaxVals[idx] = str(minVal[idx])+".."+str(maxVal[idx])

        return minMaxVals

    def _isIdentifierType(self, obj):
        return isinstance(obj, ParameterSet) or isinstance(obj, SetSet) or isinstance(obj, VariableSet)

    def _isNumberSet(self, obj):
        return isinstance(obj, BinarySet) or isinstance(obj, IntegerSet) or isinstance(obj, RealSet)

    def _isModifierSet(self, obj):
        return isinstance(obj, SymbolicSet) or isinstance(obj, LogicalSet)

    def notInTypesThatAreNotDeclarable(self, value):
        if isinstance(value, Tuple):
            return True
        
        value = value.getSymbol()
        
        return not value.isBinary and not value.isInteger and not value.isNatural and not value.isReal and not value.isSymbolic and not \
        value.isLogical and not value.isDeclaredAsVar and not value.isDeclaredAsParam and not value.isDeclaredAsSet and not \
        isinstance(value, str)

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
            selectedIndices = ",".join(selectedIndices)

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

                        posBy = domain.find("by") # if a range is inferred as the domain, the by clause is removed

                        if posBy > 0:
                            domain = domain[0:posBy].strip()

                    return op, domain, domainObj, deps, minVal, maxVal

            table = table.getParent()

        if domainAux != None:
            posIn = domainAux.find(" in ")

            if posIn > 0:
                domain = domainAux[0:posIn+4]
            else:
                domain = ""

            domains = []

            if rangeObjAux:
                
                if 0 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, maxVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(rangeObjAux[0].generateCode(self) + ".." + str(maxVal[idx]))

                        else:
                            domains.append(rangeObjAux[0].generateCode(self) + ".." + str(maxVal[indicesPosition]))

                elif 1 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, minVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(str(minVal[idx]) + ".." + rangeObjAux[1].generateCode(self))

                        else:
                            domains.append(str(minVal[indicesPosition]) + ".." + rangeObjAux[1].generateCode(self))

            else:

                if not self._isKeysInDictionary(indicesPosition, minVal) or not self._isKeysInDictionary(indicesPosition, maxVal):
                    domains = []

                else:

                    if isinstance(indicesPosition, list):
                        for idx in indicesPosition:
                            domains.append(str(minVal[idx]) + ".." + str(maxVal[idx]))

                    else:
                        domains.append(str(minVal[indicesPosition]) + ".." + str(maxVal[indicesPosition]))

            if len(domains) > 1:
                domain += "{"+", ".join(domains)+"}"

            elif len(domains) > 0:
                domain += domains[0]

            if len(domains) > 0:
                return opAux, domain, None, depsAux, minVal, maxVal

        return None, None, None, None, minVal, maxVal

    def _getSubIndicesDomainsByTables(self, name, tables, minVal, maxVal, isDeclaration = False, domainsAlreadyComputed = None, skip_outermost_scope = False):

        domain = ""
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

                domain = ""
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
                            domains[idx] = "(" + ",".join(_combIndices) + ") " + op + " " + _tuple
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
                                domains[ind] = (_subIndicesRemaining[i] + " " + subIdxDomains[i][0] + " " if not _subIndicesRemaining[i] in varNameSubIndices else "") + subIdxDomains[i][1]
                                dependencies[ind] = subIdxDomains[i][3]
                                count[ind] = 1
                                varNameSubIndices.append(_subIndicesRemaining[i])

                            else:
                                subIdxDomainsRemaining.append(ind)

                    for idx in domains:
                        if not idx in domainsAlreadyComputed or ".." in domainsAlreadyComputed[idx]:
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

            domain += ", ".join(domains_str)

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

            if domain != "" and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
                stmtIndex = stmt
                break
            
            leafs = self.symbolTables.getLeafs(stmt)
            domain, domains, dependencies, sub_indices, minVal, maxVal = self._getSubIndicesDomainsByTables(name, leafs, minVal, maxVal, isDeclaration, domainsAlreadyComputed, True)

            if domain != "" and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
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

        if domain == "":
            statements = self.symbolTables.getStatementsByKey(name)
            domain, domains, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, statements, minVal, maxVal, False)

        if domain == "":
            if minVal and maxVal and self._hasEqualIndices(minVal, maxVal):
                minMaxVals = self._zipMinMaxVals(minVal, maxVal)
                domain, domains, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, declarations, minVal, maxVal, True, minMaxVals)

                if domain == "" or domains == minMaxVals.values():
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
            self.constraintNumber += 1
            return "s.t. C" + str(self.constraintNumber) + " " + constraint.generateCode(self)
        elif isinstance(constraint, Objective):
            return self._getCodeObjective(constraint)

        return ""

    def _getIndexingExpressionFromDeclarations(self, decl):
        idxsExpression = decl.getIndexingExpression()
        _subIndices = decl.getSubIndices()

        for stmtIndex in sorted(idxsExpression, reverse=True):
            if idxsExpression[stmtIndex] and stmtIndex in _subIndices and _subIndices[stmtIndex]:
                idxExpression = idxsExpression[stmtIndex]

                return idxExpression

        return None

    def _declareVars(self):
        """
        Generate the AMPL code for the declaration of identifiers
        """

        varStr = ""
        if len(self.genVariables) > 0:
            
            graphVar = {}
            
            self._generateGraphAux(graphVar, self.genVariables)
            topological_order_var = sort_topologically_stackless(graphVar)
            
            for var in topological_order_var:

                if not self.genParameters.has(var) and not self.genSets.has(var):
                    var = self.genVariables.get(var)

                    varStr += "var " + var.getName()
                    domain = None
                    _type = None

                    varDecl = self.genDeclarations.get(var.getName())

                    domain, domains_vec, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(var.getName())

                    _types, dim, minVal, maxVal = self._getProperties(var.getName())
                    
                    if domain and domain.strip() != "":
                        logical = self._getLogicalExpressionOfDeclaration(varDecl, var.getName(), dependencies_vec, sub_indices_vec, stmtIndex)
                        varStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

                    elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0:
                        if self._hasAllIndices(minVal, maxVal):
                            domainMinMax = []
                            for i in range(len(minVal)):
                                domainMinMax.append(str(minVal[i])+".."+str(maxVal[i]))

                            domain = ", ".join(domainMinMax)
                            varStr += "{"+domain+"}"
                    
                    if not domain and varDecl != None:
                        idxExpression = self._getIndexingExpressionFromDeclarations(varDecl)
                        if idxExpression:
                            domain = idxExpression.generateCode(self)
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

                            if varDecl.getValue() != None:
                                value = ", := " + varDecl.getValue().attribute.generateCode(self)
                                varStr += value

                            elif varDecl.getDefault() != None:
                                default = ", default " + varDecl.getDefault().attribute.generateCode(self)
                                varStr += default

                    varStr += ";\n\n"

        return varStr

    def _declareParam(self, _genParameter):
        paramStr = ""
        param = _genParameter.getName()
        paramStr += "param " + param
        domain = None
        _type = None

        varDecl = self.genDeclarations.get(_genParameter.getName())

        domain, domains_vec, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(_genParameter.getName())
        _types, dim, minVal, maxVal = self._getProperties(_genParameter.getName())

        if domain != None and domain.strip() != "":
            logical = self._getLogicalExpressionOfDeclaration(varDecl, param, dependencies_vec, sub_indices_vec, stmtIndex)
            paramStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

        elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0:
            if self._hasAllIndices(minVal, maxVal):
                domainMinMax = []
                for i in range(len(minVal)):
                    domainMinMax.append(str(minVal[i])+".."+str(maxVal[i]))

                domain = ", ".join(domainMinMax)
                paramStr += "{"+domain+"}"

        if not domain and varDecl != None:
            idxExpression = self._getIndexingExpressionFromDeclarations(varDecl)
            if idxExpression:
                domain = idxExpression.generateCode(self)
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
            ins_vec = self._removePreDefinedTypes(map(lambda el: self._getSetAttribute(el.attribute), ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ", ".join(map(lambda el: "in " + el.generateCode(self), ins_vec))

                if ins != "":
                    paramStr += ", " + ins

            relations = varDecl.getRelations()
            if relations != None and len(relations) > 0:
                paramStr += ", " + ", ".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), relations))

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

        domain, domains_vec, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(_genSet.getName())
        _types, dim, minVal, maxVal = self._getProperties(_genSet.getName())

        if domain and domain.strip() != "":
            logical = self._getLogicalExpressionOfDeclaration(varDecl, _genSet.getName(), dependencies_vec, sub_indices_vec, stmtIndex)
            setStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"

        elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0:
            if self._hasAllIndices(minVal, maxVal):
                domainMinMax = []
                for i in range(len(minVal)):
                    domainMinMax.append(str(minVal[i])+".."+str(maxVal[i]))

                domain = ", ".join(domainMinMax)
                setStr += "{"+domain+"}"

        if not domain and varDecl != None:
            idxExpression = self._getIndexingExpressionFromDeclarations(varDecl)
            if idxExpression:
                domain = idxExpression.generateCode(self)
                setStr += "{" + domain + "}"
        
        if dim != None and dim > 1:
            setStr += " dimen " + str(dim)

        if varDecl != None:
            subsets = varDecl.getWithin()
            if subsets != None and len(subsets) > 0:
                setStr += ", " + ", ".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), subsets))

            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: self._getSetAttribute(el.attribute), ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ", ".join(map(lambda el: "in " + el.generateCode(self), ins_vec))

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
        res = ""

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
        
        res += self._posModel()

        return res

    # Objectives
    def generateCode_Objectives(self, node):
        self.totalObjectives = len(node.objectives)
        return "\n\n".join(map(self._getCodeObjective, node.objectives))

    # Objective Function
    def generateCode_Objective(self, node):
        """
        Generate the code in AMPL for this Objective
        """
        
        domain_str = ""
        if node.domain:
            idxExpression = node.domain.generateCode(self)
            if idxExpression:
                domain_str = " {" + idxExpression + "}"

        return node.type + " obj" + (str(self.objectiveNumber) if self.objectiveNumber > 1 else "")  + domain_str + ": " + node.linearExpression.generateCode(self) + ";"

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
        res = node.linearExpression1.generateCode(self) + " " + node.op + " " + node.linearExpression2.generateCode(self)
        return res

    def generateCode_ConstraintExpression3(self, node):
        res = node.numericExpression1.generateCode(self) + " " + node.op + " " + node.linearExpression.generateCode(self) + " " + node.op + " " + node.numericExpression2.generateCode(self)
        return res

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
            supExpression = self._getValueFromNumericExpression(node.numericExpression)

            if isinstance(supExpression, Identifier) or isinstance(supExpression, Number):
                supExpression = supExpression.generateCode(self)
            else:
                supExpression = "(" + supExpression.generateCode(self) + ")"

            res = SUM + "{" + node.indexingExpression.generateCode(self) + ".."+supExpression+"}"
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
        if not isinstance(node.function, str):
            function = node.function.generateCode(self)
        else:
            function = node.function

        res = function + "("

        if node.numericExpression1 != None:
            res += node.numericExpression1.generateCode(self)

        if node.numericExpression2 != None:
            res += ", " + node.numericExpression2.generateCode(self)

        res += ")"

        return res

    def generateCode_FractionalNumericExpression(self, node):
        
        numerator = node.numerator
        if isinstance(node.numerator, ValuedNumericExpression):
            numerator = numerator.value
            
        if not isinstance(numerator, Identifier) and not isinstance(numerator, Number):
            numerator = "("+numerator.generateCode(self)+")"
        else:
            numerator = numerator.generateCode(self)
            
        denominator = node.denominator
        if isinstance(denominator, ValuedNumericExpression):
            denominator = denominator.value
            
        if not isinstance(denominator, Identifier) and not isinstance(denominator, Number):
            denominator = "("+denominator.generateCode(self)+")"
        else:
            denominator = denominator.generateCode(self)
            
        return numerator+"/"+denominator
        
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
            
            supExpression = self._getValueFromNumericExpression(node.supNumericExpression)

            if isinstance(supExpression, Identifier) or isinstance(supExpression, Number):
                supExpression = supExpression.generateCode(self)
            else:
                supExpression = "(" + supExpression.generateCode(self) + ")"

            res = str(node.op) + "{" + node.indexingExpression.generateCode(self) + ".."+supExpression+"}"
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

        if node.function == SymbolicExpressionWithFunction.SPRINTF:
            res += node.firstExpression.generateCode(self) + "," + node.numericExpression1.generateCode(self)

        elif node.function == SymbolicExpressionWithFunction.CTIME:
            if node.firstExpression != None:
                res += node.firstExpression.generateCode(self)

        elif node.function == SymbolicExpressionWithFunction.ALIAS or node.function == SymbolicExpressionWithFunction.CHAR:
            res += node.firstExpression.generateCode(self)

        elif node.function == SymbolicExpressionWithFunction.SUBSTR or node.function == SymbolicExpressionWithFunction.SUB or node.function == SymbolicExpressionWithFunction.GSUB:
            res += node.firstExpression.generateCode(self) + "," + node.numericExpression1.generateCode(self)
            if node.numericExpression2 != None:
                res += "," + node.numericExpression2.generateCode(self)
                
        elif node.function == SymbolicExpressionWithFunction.TIME2STR:
            res += node.firstExpression.generateCode(self) + "," + node.numericExpression1.generateCode(self)

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
        res = node.op

        if node.supExpression:
            supExpression = self._getValueFromNumericExpression(node.supExpression)

            if isinstance(supExpression, Identifier) or isinstance(supExpression, Number):
                supExpression = supExpression.generateCode(self)
            else:
                supExpression = "(" + supExpression.generateCode(self) + ")"

            res += " {" + node.indexingExpression.generateCode(self) + ".."+supExpression+"} "
        else:
            res += " {" + node.indexingExpression.generateCode(self) + "} "

        res += node.integrand.generateCode(self)

        return res

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

    # IntegerSet
    def generateCode_IntegerSet(self, node):
        res = "integer"
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = ""
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += ", "
            else:
                op += " "
                
            op += node.firstOp+" "
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = ""
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += ", "
            else:
                op += " "
                
            op += node.secondOp+" "
            
            res += op + secondBound
            
        return res

    # RealSet
    def generateCode_RealSet(self, node):
        res = ""
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = ""
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += ", "
                
            op += node.firstOp+" "
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = ""
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += ", "
                
            op += node.secondOp+" "
            
            res += op + secondBound
            
        return res

    # BinarySet
    def generateCode_BinarySet(self, node):
        return "binary"

    # SymbolicSet
    def generateCode_SymbolicSet(self, node):
        return "symbolic"

    # LogicalSet
    def generateCode_LogicalSet(self, node):
        return "logical"

    # ParameterSet
    def generateCode_ParameterSet(self, node):
        return ""

    # SymbolicSet
    def generateCode_VariableSet(self, node):
        return ""

    # SetSet
    def generateCode_SetSet(self, node):
        return ""
