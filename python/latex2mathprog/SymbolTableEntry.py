class SymbolTableEntry(object):
    def __init__(self, key, properties, _type, scope, sub_indices = [], inferred = True, isDefined = False):
        """
        Constructor
        
        :param key         : string
        :param properties  : GenProperties
        :param _type       : CONSTANTS.VARIABLES | CONSTANTS.PARAMETERS | CONSTANTS.SETS
        :param scope       : int
        :param sub_indices : [string]
        :param inferred    : boolean
        :param isDefined   : boolean
        
        """

        self.key = key
        self.properties = properties
        self.type = _type
        self.scope = scope
        self.inferred = inferred
        self.isDefined = isDefined

        # python bug
        if len(sub_indices) == 0:
            self.sub_indices = []
        else:
            self.sub_indices = sub_indices

    def __len__(self):
        return 1

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def setProperties(self, properties):
        self.properties = properties

    def getProperties(self):
        return self.properties

    def setType(self, _type):
        self.type = _type

    def getType(self):
        return self.type

    def setScope(self, scope):
        self.scope = scope

    def getScope(self):
        return self.scope

    def setInferred(self, inferred):
        self.inferred = inferred

    def getInferred(self):
        return self.inferred

    def setIsDefined(self, isDefined):
        self.isDefined = isDefined

    def getIsDefined(self):
        return self.isDefined

    def setSubIndices(self, sub_indices):
        self.sub_indices = sub_indices

    def getSubIndices(self):
        return self.sub_indices

    def addSubIndices(self, sub_indices):
        for sub_indice in self.sub_indices:
            if list(sub_indice) == list(sub_indices):
                # remove and add again to keep the order from last to first position (in the statement) of these Identifier's s sub-indices
                self.sub_indices.remove(sub_indice) 

        self.sub_indices.append(sub_indices)
