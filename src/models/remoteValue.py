class RemoteValue():

    def __init__(self, remoteValueType, initValue):
        self.remoteValueType = remoteValueType
        self.value = initValue

    def set(self, value):
        self.value = value

    def get(self):
        return self.value
    
    def getRemoteValue(type, remoteValues):
        return next((x for x in remoteValues if x.remoteValueType == type), None)
