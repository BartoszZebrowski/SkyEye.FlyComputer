
from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from states.state import State
import cv2


class ManualState(State):

    def __init__(self, serialClient, remoteVariables, camera, outputStream):
        self.serialClient = serialClient
        self.remoteVariables = remoteVariables
        self.camera = camera
        self.outputStream = outputStream

        super().__init__()

    def execute(self):
        # print("ManualSate")
        self.processImage()

        # vericalAxis = RemoteVariable.getRemoteVariable(RemoteVariableType.VerticalAxis, self.remoteVariables)
        # self.serialClient.setValue(RemoteVariableType.VerticalAxis, vericalAxis)

    def processImage(self):
        frame = self.camera.read()

        frame[:,:,1] = 0
        
        self.outputStream.write(frame)        



