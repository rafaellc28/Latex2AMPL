from SymbolTable import *
from Constants import *

class SymbolTables(object):
    def __init__(self):
        """
        Constructor
        """

        self.tables = {}
        self.types = [Constants.PARAMETERS, Constants.VARIABLES, Constants.SETS]

    def __len__(self):
        return len(self.tables)

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return self.tables.iteritems()

    def insert(self, statement, table, level = 0, isDeclaration = False):
        if not statement in self.tables:
            self.tables[statement] = {"lastScope": 0, "isDeclaration": isDeclaration, "tables": [{"scope": 0, "level": level, "table": table}]}
        else:
            self.tables[statement]["lastScope"] += 1
            table.setScope(self.tables[statement]["lastScope"])
            self.tables[statement]["tables"].append({"scope": self.tables[statement]["lastScope"] , "level": level, "table": table})
        
        return table

    def lookup(self, statement, scope = 0):
        if not statement in self.tables:
            return None

        for table in self.tables[statement]["tables"]:
            if table["scope"] == scope:
                return table["table"]

        return None

    def lastLevel(self, statement):
        if not statement in self.tables:
            return None

        levels = []
        for table in self.tables[statement]["tables"]:
            levels.append(table["level"])

        return max(levels)

    def getStatements(self):
        statements = {k: v for k, v in self.tables.iteritems()}
        return statements

    def getStatementsByKey(self, key):
        statements = self.getStatements()
        return {k:v for k,v in statements.iteritems() for k2 in [k1 for k1 in [t["table"].getTable() for t in v["tables"]]] if key in k2}

    def getDeclarations(self):
        declarations = {k: v for k, v in self.tables.iteritems() if v["isDeclaration"]}
        return declarations

    def getDeclarationsByStatement(self, statement):
        declarations = self.getDeclarations()
        return {k:v for k,v in declarations.iteritems() if k == statement}
    
    def getDeclarationsByKey(self, key):
        declarations = self.getDeclarations()
        return {k:v for k,v in declarations.iteritems() for k2 in [k1 for k1 in [t["table"].getTable() for t in v["tables"]]] if key in k2}

    def getDeclarationsWhereKeyIsDefined(self, key):
        #declarations = self.getDeclarationsByKey(key)
        #print(declarations)
        res = {}
        declarations = self.getDeclarations()
        for k, decl in declarations.iteritems():
            inserted = False
            for t in decl["tables"]:
                table = t["table"].getTable()
                for k1,v1 in table.iteritems():
                    if k1 == key and v1.getIsDefined(): #v1.getType() in self.types:
                        res[k] = decl
                        inserted = True
                        break

                if inserted:
                    break

        return res

    def getDeclarationsWhereKeyIsUsed(self, key):
        #declarations = self.getDeclarationsByKey(key)
        
        res = {}
        declarations = self.getDeclarations()
        for k,decl in declarations.iteritems():
            inserted = False
            for t in decl["tables"]:
                table = t["table"].getTable()
                for k1,v1 in table.iteritems():
                    if k1 == key and not v1.getIsDefined(): #v1.getType() == None:
                        res[k] = decl
                        inserted = True
                        break

                if inserted:
                    break

        return res
        
        #declarations = self.getDeclarationsByKey(key)
        #return {k:v for k,v in declarations.iteritems() for k1,v1 in {k2:v2 for t in v["tables"] for k2,v2 in t["table"].getTable().iteritems()} if v1.getType() == None}

    def getConstraints(self):
        constraints = {k: v for k, v in self.tables.iteritems() if not v["isDeclaration"]}
        return constraints

    def getConstraintsByStatement(self, statement):
        constraints = self.getConstraints()
        return {k:v for k,v in constraints.iteritems() if k == statement}

    def getConstraintsByKey(self, key):
        constraints = self.getConstraints()
        return {k:v for k,v in constraints.iteritems() for k2 in [k1 for k1 in [t["table"].getTable() for t in v["tables"]]] if key in k2}

    def getLeafs(self, statement):
        leafs = [table for table in self.tables[statement]["tables"] if table["table"].getIsLeaf()]
        return leafs

    def getScopesWhereKeyIsDefined(self, key, statement):
        scopes = []
        for table in self.tables[statement]["tables"]:
            for k1,v1 in table["table"].getTable().iteritems():
                if k1 == key and v1.getIsDefined(): #v1.getType() == None:
                    scopes.append(table)
                    break
        
        return scopes

    def getFirstScopeByKey(self, key, statement):
        scopes = []
        for table in self.tables[statement]["tables"]:
            for k1,v1 in table["table"].getTable().iteritems():
                if k1 == key and table["scope"] == 0: #v1.getType() == None:
                    scopes.append(table)
                    break
        
        return scopes
