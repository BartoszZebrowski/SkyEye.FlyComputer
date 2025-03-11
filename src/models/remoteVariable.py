class RemoteVariable():

    def __init__(self, remoteVariableType, initValue):
        self.remoteVariableType = remoteVariableType
        self.value = initValue
        self.toRefresh = True

    def set(self, value):
        value = value
        self.toRefresh = True

    def get(self):
        return self.value