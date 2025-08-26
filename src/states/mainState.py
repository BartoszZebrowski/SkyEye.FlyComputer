from models.remoteValue import *
from models.remoteValueType import *
from states.state import State
import cv2
import machineVisionTools as mv


## @class MainState
#  @brief Klasa reprezentująca główny stan aplikacji odpowiedzialny za przetwarzanie obrazu.
class MainState(State):

    ## @brief Konstruktor stanu głównego.
    #  @param remoteValues Lista wartości zdalnych.
    #  @param camera Obiekt kamery służący do odczytu obrazu.
    #  @param outputStream Strumień wyjściowy do zapisu przetworzonego obrazu.
    def __init__(self, remoteValues, camera, outputStream):
        self.remoteValues = remoteValues
        self.camera = camera
        self.outputStream = outputStream
        self.zoomValue = remoteValue.getremoteValue(remoteValueType.ZoomValue, self.remoteValues)

        super().__init__()

    ## @brief Wykonuje główną logikę stanu.
    def execute(self):
        self.processImage()

    ## @brief Przetwarza obraz z kamery: powiększa, skaluje, obraca i stabilizuje.
    def processImage(self):
        frame = self.camera.read()

        frame = mv.zoomToCenter(frame, self.zoomValue.get())
        scaled_image = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_CUBIC)
        rotated_image = cv2.flip(scaled_image, -1)

        stabilizeImage = mv.stabilizeImageRoll(rotatedImage, RemoteValueType.ActualRollValue)

        self.outputStream.write(stabilizeImage)
