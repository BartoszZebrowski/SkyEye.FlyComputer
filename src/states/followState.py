
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
        self.processImage()

    def processImage(self):
        frame = self.camera.read()

        frame[:,:,2] = 0

        scaled_image = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_CUBIC)

        self.outputStream.write(frame)        