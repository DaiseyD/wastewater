


class DataTarget:
    target= {}
    data = None
    instance = None
    def __new__(self): # creation pattern for a singleton, init is not called during the creation
        if self.instance==None:
            cls = super().__new__(self)
            self.instance = cls
            return cls
        else: 
            return self.instance
        
    def setData(self, data):
        if self.data!=None:
            raise Exception("not allowed to rewrite data to singleton")
        else:
            self.data = data
            self.initializeTarget()

    def initializeTarget(self):
        self.target['parameters'] = {}
        self.target['rainfallevents'] = []
        self.target['simparameters'] = {}


    def updateParameterField(self, parameterName, fieldName, values, strategy):
        if parameterName not in self.target['parameters']:
            self.target['parameters'][parameterName] = {}
        self.target['parameters'][parameterName][fieldName] = { "values": values, "strategy": strategy} 
    
    def removeFromParameterField(self, parameterName, fieldName):
        if parameterName in self.target['parameters'] and fieldName in self.target['parameters'][parameterName]:
            self.target['parameters'][parameterName].remove(fieldName)
            if self.target['parameters'][parameterName] == {}:
                self.target['parameters'].remove(parameterName)
    
    








