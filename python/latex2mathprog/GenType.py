from GenObj import *

class GenType(GenObj):
    def __init__(self, name, _type = None, minVal = None, maxVal = None, dimension = None):
        """
        Constructor
        
        :param name      : string
        :param _type     : string
        :param dimension : int
        :param minVal    : float
        :param maxVal    : float
        """
        
        super(GenType, self).__init__(name)
        self.type = _type
        self.minVal = minVal
        self.maxVal = maxVal
        self.dimension = dimension

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
    
    def getType(self):
        return self.type

    def setType(self, _type):
        self.type = _type

    def setDimension(self, dimension):
        self.dimension = dimension

    def getDimension(self):
        return self.dimension

    def getMinVal(self):
        return self.minVal

    def setMinVal(self, minVal):
        if self.minVal == None or minVal < self.minVal:
            self.minVal = minVal

    def getMaxVal(self):
        return self.maxVal

    def setMaxVal(self, maxVal):
        if self.maxVal == None or maxVal > self.maxVal:
            self.maxVal = minVal
