from GenObj import *

class GenItemDomain(GenObj):

    def __init__(self, name, op, dependencies = [], obj = None):
        """
        Constructor
        
        :param name         : string
        :param op           : string
        :param dependencies : [string]
        :param obj          : object
        """
        
        super(GenItemDomain, self).__init__(name)
        self.op = op
        
        # python bug
        if len(dependencies) == 0:
            self.dependencies = []
        else:
            self.dependencies = dependencies
            
        self.obj = obj
        
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name
        
    def setOp(self, op):
        self.op = op
        
    def getOp(self):
        return self.op
        
    def setDependencies(self, dependencies):
        self.dependencies = dependencies
        
    def getDependencies(self):
        return self.dependencies
        
    def addDependency(self, dependency):
        for d in self.dependencies:
            if d == dependency:
                # remove and add again to keep the order from last to first position (in the statement) of these domain's dependencies
                self.dependencies.remove(d)
                
        self.dependencies.append(dependency)
        
    def setObj(self, obj):
        self.obj = obj
        
    def getObj(self):
        return self.obj
    