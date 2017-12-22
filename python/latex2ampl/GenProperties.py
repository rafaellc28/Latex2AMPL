from GenObj import *

class GenProperties(GenObj):
    def __init__(self, name, domains = [], dimension = None, minVal = {}, maxVal = {}, default = None, attributes = None):
        """
        Constructor
        
        :param name       : string
        :param domains    : [GenItemDomain]
        :param dimension  : int
        :param minVal     : {int: int} - {index: minVal}
        :param maxVal     : {int: int} - {index: maxVal}
        :param default    : default
        :param attributes : attributes
        """
        
        super(GenProperties, self).__init__(name)

        # python bug
        if len(domains) == 0:
            self.domains = []
        else:
            self.domains = domains

        if minVal == None or len(minVal) == 0:
            self.minVal = {}
        else:
            self.minVal = minVal

        if maxVal == None or len(maxVal) == 0:
            self.maxVal = {}
        else:
            self.maxVal = maxVal

        self.dimension = dimension
        self.default = default
        self.attributes = attributes

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getDomains(self):
        return self.domains

    def addDomain(self, domain):
        for d in self.domains:
            if d.getName() == domain.getName():
                # remove and add again to keep the order from last to first position (in the statement) of these Identifier's domains
                self.domains.remove(d)

        self.domains.append(domain)

    def setDomains(self, domains):
        self.domains = domains

    def setDimension(self, dimension):
        self.dimension = dimension

    def getDimension(self):
        return self.dimension

    def setMinVal(self, minVal):
        self.minVal = minVal

    def getMinVal(self):
        return self.minVal

    def setMinValByIndex(self, index, val):
        if not index in self.minVal or val < self.minVal[index]:
            self.minVal[index] = val

    def getMinValByIndex(self, index):
        if index in self.minVal:
            return self.minVal[index]

        return None

    def setMaxVal(self, maxVal):
        self.maxVal = maxVal

    def getMaxVal(self):
        return self.maxVal

    def setMaxValByIndex(self, index, val):
        if not index in self.maxVal or val > self.maxVal[index]:
            self.maxVal[index] = val
            
    def getMaxValByIndex(self, index):
        if index in self.maxVal:
            return self.maxVal[index]

        return None

    def getDefault(self):
        return self.default

    def setDefault(self, default):
        self.default = default

    def getAttributes(self):
        return self.attributes

    def setAttributes(self, attributes):
        self.attributes = attributes
