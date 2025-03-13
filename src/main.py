import atexit
import threading
import cv2
import nanocamera as nano

from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from serialClient import SerialClient
from tcpServer import TcpServer
from states.followState import FollowState
from states.manualState import ManualState
from states.stateMachine import StateMachine 

host = "192.168.1.27"
port = 9002
width = 1280
height = 720
fps = 30

# cos tam dziala
pipeline = (
    f'appsrc is-live=true !'
    f'videoconvert ! nvvidconv !'
    f'nvv4l2h264enc ! h264parse ! '
    f'rtph264pay config-interval=1 pt=96 ! udpsink host={host} port={port} sync=false'
)

# pipeline = (
#     f'appsrc ! videoconvert ! video/x-raw,format=BGR ! '
#     f'videoconvert ! x264enc ! h264parse ! '
#     f'rtph264pay config-interval=1 pt=96 ! udpsink host={host} port={port} sync=false'
# )




camera = nano.Camera(camera_type=0, device_id=0, debug=True, width=1280, height=720)

serialClient = SerialClient("COM9", 9600, 1)
# videoIn = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
videoOut = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, fps, (width, height))

remoteVariablesLock = threading.Lock()
remoteVariables = [
    RemoteVariable(RemoteVariableType.HorisonalAxis.value, 0),
    RemoteVariable(RemoteVariableType.VerticalAxis.value, 0),
    RemoteVariable(RemoteVariableType.WorkingMode.value, 0),
]

states = [
    ManualState(serialClient, remoteVariables, camera, videoOut),
    FollowState()
]



server = TcpServer(5001, remoteVariables, remoteVariablesLock)
serverThread = threading.Thread(target=lambda: server.start())

statemachine = StateMachine(states, RemoteVariable.getRemoteVariable(RemoteVariableType.WorkingMode, remoteVariables))
stateMachineThread = threading.Thread(target=lambda: statemachine.start())

# serialClient = SerialClient

serverThread.start()
stateMachineThread.start()

print("Dziala")

def onExit():
    camera.release()
    videoOut.release()
    cv2.destroyAllWindows()

atexit.register(onExit)