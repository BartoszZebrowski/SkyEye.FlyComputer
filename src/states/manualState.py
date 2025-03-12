
from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from states.state import State
import cv2


class ManualState(State):

    def __init__(self, serialClient, remoteVariables, videoIn, videoOut):
        self.serialClient = serialClient
        self.remoteVariables = remoteVariables
        self.videoIn = videoIn
        self.videoOut = videoOut

        super().__init__()

    def execute(self):
        print("ManualSate")
        self.processImage(self)

        # vericalAxis = RemoteVariable.getRemoteVariable(RemoteVariableType.VerticalAxis, self.remoteVariables)
        # self.serialClient.setValue(RemoteVariableType.VerticalAxis, vericalAxis)

    def processImage(self):
        ret, frame = self.videoIn.read()
        self.videoOut.write(frame)        



