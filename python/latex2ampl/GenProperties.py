from GenObj import *

class GenProperties(GenObj):
    def __init__(self, name, domains = [], dimension = None, minVal = None, maxVal = None, default = None, attributes = None):
        """
        Constructor
        
        :param name       : string
        :param domains    : [GenItemDomain]
        :param dimension  : int
        :param minVal     : float
        :param maxVal     : float
        :param default    : default
        :param attributes : attributes
        """
        
        super(GenProperties, self).__init__(name)

        # python bug
        if len(domains) == 0:
            self.domains = []
        else:
            self.domains = domains

        self.dimension = dimension
        self.minVal = minVal
        self.maxVal = maxVal
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

    def setMaxVal(self, maxVal):
        self.maxVal = maxVal

    def getMaxVal(self):
        return self.maxVal

    def getDefault(self):
        return self.default

    def setDefault(self, default):
        self.default = default

    def getAttributes(self):
        return self.attributes

    def setAttributes(self, attributes):
        self.attributes = attributes

    '''
    def addAttributes(self, attributes):
        if self.attributes == None:
            self.attributes = []

        if isinstance(attributes, list):
            self.attributes += attributes
        else:
            self.attributes.append(attributes)
    '''