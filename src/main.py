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
bitrate = 5_000_000
fps = 30

com = "COM9"
baudrate = 9600
timeout = 1

tcpPort = 5001

pipeline = (
    f'appsrc is-live=true !'
    f'videoconvert ! nvvidconv !'
    f'nvv4l2h264enc bitrate={bitrate} ! h264parse ! '
    f'rtph264pay config-interval=1 pt=96 ! udpsink host={host} port={port} sync=false'
)

serialClient = SerialClient("COM9", 9600, 1)

camera = nano.Camera(camera_type=0, device_id=0, debug=True, width=width, height=height)
outputStream = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, fps, (width, height))

remoteVariablesLock = threading.Lock()
remoteVariables = [
    RemoteVariable(RemoteVariableType.WorkingMode, 0),
    RemoteVariable(RemoteVariableType.TargetHorizontalAngle, 0),
    RemoteVariable(RemoteVariableType.TargetVerticalAngle, 0),
    RemoteVariable(RemoteVariableType.ActualHorizontaAngle, 0),
    RemoteVariable(RemoteVariableType.ActualVerticalAngle, 0),
]

states = [
    ManualState(serialClient, remoteVariables, camera, outputStream),
    FollowState(serialClient, remoteVariables, camera, outputStream)
]

tcpServer = TcpServer(tcpPort, remoteVariables, remoteVariablesLock)
serverThread = threading.Thread(target=lambda: tcpServer.start())

statemachine = StateMachine(states, RemoteVariable.getRemoteVariable(RemoteVariableType.WorkingMode, remoteVariables))
stateMachineThread = threading.Thread(target=lambda: statemachine.start())

serverThread.start()
stateMachineThread.start()

print("Dziala")

def onExit():
    camera.release()
    outputStream.release()
    tcpServer.stop()

atexit.register(onExit)