from models.remoteValue import *
from models.remoteValueType import *
from states.state import State
import cv2
import machineVisionTools as mv


class MainState(State):

    def __init__(self, remoteValues, camera, outputStream):
        self.remoteValues = remoteValues
        self.camera = camera
        self.outputStream = outputStream
        self.zoomValue = remoteValue.getremoteValue(remoteValueType.ZoomValue, self.remoteValues)

        super().__init__()

    def execute(self):
        self.processImage()

    def processImage(self):
        frame = self.camera.read()

        frame = mv.zoomToCenter(frame, self.zoomValue.get())
        scaled_image = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_CUBIC)
        rotated_image = cv2.flip(scaled_image, -1)

        stabilizeImage = mv.stabilizeImageRoll(rotatedImage, RemoteValueType.ActualRollValue)

        self.outputStream.write(stabilizeImage)
