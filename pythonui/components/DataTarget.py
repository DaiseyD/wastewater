

# Singleton class used for controlling access to the infoworks data and datatarget
class DataTarget:
    observers = [] 
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
            self.__initializeTarget()

    def __initializeTarget(self):
        self.target['parameters'] = {}
        self.target['rainfallevents'] = []
        self.target['simparameters'] = {}

    def updateParameterField(self, parameterName, fieldName, values, strategy):
        if parameterName not in self.target['parameters']:
            self.target['parameters'][parameterName] = {}
        self.target['parameters'][parameterName][fieldName] = { "values": values, "strategy": strategy} 
        self.updateObservers()

    def removeFromParameterField(self, parameterName, fieldName):
        if parameterName in self.target['parameters'] and fieldName in self.target['parameters'][parameterName]:
            self.target['parameters'][parameterName].pop(fieldName)
            if self.target['parameters'][parameterName] == {}:
                self.target['parameters'].pop(parameterName)
        self.updateObservers()
    
    def addToRain(self, rainid):
        self.target['rainfallevents'].append(rainid)
        self.updateObservers()
    
    def removeFromRain(self, rainid):
        self.target['rainfallevents'].remove(rainid)
        self.updateObservers()

    def updateSimParameters(self, key, value):
        self.updateObservers()

    def updateObservers(self):
        for i in self.observers:
            i.update()
