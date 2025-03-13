
from states.state import State
import cv2

class FollowState(State):

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

        frame[:,:,2] = 0

        self.outputStream.write(frame)        