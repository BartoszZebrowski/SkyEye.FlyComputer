import atexit
import threading
import cv2
import nanocamera as nano

from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from serialServer import SerialServer
from tcpServer import TcpServer
from states.followState import FollowState
from states.manualState import ManualState
from states.stateMachine import StateMachine 
from udpServer import UdpServer

host = "192.168.1.27"
port = 9002
width = 1280
height = 720
bitrate = 10_000_000
fps = 30

com = "/dev/ttyUSB1"
baudrate = 115200
timeout = 1

tcpPort = 5001

pipeline = (
    f'appsrc is-live=true !'
    f'videoconvert ! nvvidconv !'
    f'nvv4l2h264enc bitrate={bitrate} ! h264parse ! '
    f'rtph264pay config-interval=1 pt=96 ! udpsink host={host} port={port} sync=false'
)

camera = nano.Camera(camera_type=0, device_id=0, debug=True, width=1280, height=720)
outputStream = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, fps, (1280, 720))

remoteVariablesLock = threading.Lock()
remoteVariables = [
    RemoteVariable(RemoteVariableType.Ping, 0),
    RemoteVariable(RemoteVariableType.WorkingMode, 0),
    RemoteVariable(RemoteVariableType.TargetHorizontalAngle, 0),
    RemoteVariable(RemoteVariableType.TargetVerticalAngle, 0),
    RemoteVariable(RemoteVariableType.ActualHorizontaAngle, 0),
    RemoteVariable(RemoteVariableType.ActualVerticalAngle, 0),
    RemoteVariable(RemoteVariableType.ZoomValue, 1),
]

states = [
    ManualState(remoteVariables, camera, outputStream),
    FollowState(remoteVariables, camera, outputStream)
]

udpServer = UdpServer(tcpPort, remoteVariables, remoteVariablesLock)
udpServerThread = threading.Thread(target=lambda: udpServer.start())

serialServer = SerialServer(com, baudrate, timeout, remoteVariables, remoteVariablesLock)
serialServerThread = threading.Thread(target=lambda: serialServer.start())

statemachine = StateMachine(states, RemoteVariable.getRemoteVariable(RemoteVariableType.WorkingMode, remoteVariables))
stateMachineThread = threading.Thread(target=lambda: statemachine.start())

udpServerThread.start()
serialServerThread.start()
stateMachineThread.start()

print("Program started")

def onExit():
    camera.release()
    outputStream.release()
    udpServer.stop()
    serialServer.stop()

atexit.register(onExit)