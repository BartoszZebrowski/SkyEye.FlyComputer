import atexit
import threading
import cv2

from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from serialClient import SerialClient
from tcpServer import TcpServer
from states.followState import FollowState
from states.manualState import ManualState
from states.stateMachine import StateMachine 

streamPipeline = (
    "appsrc ! videoconvert ! video/x-raw,format=I420 ! "
    "nvvidconv ! nvv4l2h264enc insert-sps-pps=true bitrate=4000000 ! "
    "h264parse ! rtph264pay pt=96 ! "
    "udpsink host=192.168.1.27 port=9002 sync=false"
)

serialClient = SerialClient("COM9", 9600, 1)
videoIn = cv2.VideoCapture(0)
videoOut = cv2.VideoWriter(streamPipeline, cv2.CAP_GSTREAMER, 0, 30, (1920, 1080), True)

remoteVariablesLock = threading.Lock()
remoteVariables = [
    RemoteVariable(RemoteVariableType.HorisonalAxis.value, 0),
    RemoteVariable(RemoteVariableType.VerticalAxis.value, 0),
    RemoteVariable(RemoteVariableType.WorkingMode.value, 0),
]

states = [
    FollowState(),
    ManualState(serialClient, remoteVariables, videoIn, videoOut)
]



## zadbac o wielowatkowosc
server = TcpServer(5001, remoteVariables, remoteVariablesLock)
serverThread = threading.Thread(target=lambda: server.start())

statemachine = StateMachine(states, RemoteVariable.getRemoteVariable(RemoteVariableType.WorkingMode, remoteVariables))
stateMachineThread = threading.Thread(target=lambda: statemachine.start())

# serialClient = SerialClient

serverThread.start()
stateMachineThread.start()

print("Dziala")

def onExit():
    videoIn.release()
    videoOut.release()
    cv2.destroyAllWindows()

atexit.register(onExit)