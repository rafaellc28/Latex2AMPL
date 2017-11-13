class SymbolTable(object):
    def __init__(self, statement = 0, parent = None, isLeaf = True, scope = 0):
        """
        Constructor
        
        :param statement: int
        :param parent   : SymbolTable
        :param isLeaf   : bool
        """
        
        self.table = {}
        self.statement = statement
        self.parent = parent
        self.isLeaf = isLeaf
        self.scope = scope

    def __len__(self):
        return len(self.table)

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return self.table.iteritems()

    def insert(self, key, value):
        self.table[key] = value

    def lookup(self, key):
        if key in self.table:
            return self.table[key]

        return None

    def setStatement(self, statement):
        self.statement = statement

    def getStatement(self):
        return self.statement

    def setParent(self):
        self.parent = parent

    def getParent(self):
        return self.parent

    def setIsLeaf(self, isLeaf):
        self.isLeaf = isLeaf

    def getIsLeaf(self):
        return self.isLeaf

    def setScope(self, scope):
        self.scope = scope

    def getScope(self):
        return self.scope

    def getTable(self):
        return self.table
