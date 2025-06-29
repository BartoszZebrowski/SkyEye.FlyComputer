class RemoteVariable():

    def __init__(self, remoteVariableType, initValue):
        self.remoteVariableType = remoteVariableType
        self.value = initValue

    def set(self, value):
        self.value = value

    def get(self):
        return self.value
    
    def getRemoteVariable(type, remoteVariables):
        return next((x for x in remoteVariables if x.remoteVariableType == type), None)
