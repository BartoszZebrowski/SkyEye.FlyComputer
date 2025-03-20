
from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from states.state import State
import cv2
import machineVisionTools as mv


class ManualState(State):

    def __init__(self, serialClient, remoteVariables, camera, outputStream):
        self.serialClient = serialClient
        self.remoteVariables = remoteVariables
        self.camera = camera
        self.outputStream = outputStream
        self.zoomValue = RemoteVariable.getRemoteVariable(RemoteVariableType.ZoomValue, self.remoteVariables)

        super().__init__()

    def execute(self):
        self.processImage()

    def processImage(self):
        frame = self.camera.read()

        frame = mv.zoomToCenter(frame, self.zoomValue.get())
        scaled_image = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_CUBIC)

        self.outputStream.write(scaled_image)
