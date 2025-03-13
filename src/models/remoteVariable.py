class RemoteVariable():

    def __init__(self, remoteVariableType, initValue):
        self.remoteVariableType = remoteVariableType
        self.value = initValue
        self.toRefresh = True

    def set(self, value):
        self.value = value
        print(f"Prawdziwa wartosc {self.value}")
        self.toRefresh = True

    def get(self):
        return self.value
    
    def getRemoteVariable(type, remoteVariables):
        return next((x for x in remoteVariables if x.remoteVariableType == type), None)
