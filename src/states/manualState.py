
from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from states.state import State
import cv2


class ManualState(State):

    def __init__(self, serialClient, remoteVariables, camera, videoOut):
        self.serialClient = serialClient
        self.remoteVariables = remoteVariables
        self.camera = camera
        self.videoOut = videoOut

        super().__init__()

    def execute(self):
        # print("ManualSate")
        self.processImage()

        # vericalAxis = RemoteVariable.getRemoteVariable(RemoteVariableType.VerticalAxis, self.remoteVariables)
        # self.serialClient.setValue(RemoteVariableType.VerticalAxis, vericalAxis)

    def processImage(self):
        frame = self.camera.read()
        # print(frame.shape)
        self.videoOut.write(frame)        



