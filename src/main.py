import atexit
import threading
import cv2
import nanocamera as nano

from models.remoteValue import *
from models.remoteValueType import *
from serialServer import SerialServer
from tcpServer import TcpServer
from states.mainState import MainState
from states.stateMachine import StateMachine 
from udpServer import UdpServer

host = "192.168.1.27"
port = 9002
width = 1280
height = 720
bitrate = 10_000_000
fps = 30

com = "/dev/ttyUSB0"
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

remoteValuesLock = threading.Lock()
remoteValues = [
    RemoteValue(RemoteValueType.Ping, 0),
    RemoteValue(RemoteValueType.WorkingMode, 0),
    RemoteValue(RemoteValueType.TargetHorizontalAngle, 0),
    RemoteValue(RemoteValueType.TargetVerticalAngle, 0),
    RemoteValue(RemoteValueType.ActualHorizontaAngle, 0),
    RemoteValue(RemoteValueType.ActualVerticalAngle, 0),
    RemoteValue(RemoteValueType.ZoomValue, 1),
]

states = [
    MainState(remoteValues, camera, outputStream),
]

udpServer = UdpServer(tcpPort, remoteValues, remoteValuesLock)
udpServerThread = threading.Thread(target=lambda: udpServer.start())

# serialServer = SerialServer(com, baudrate, timeout, remoteValues, remoteValuesLock)
# serialServerThread = threading.Thread(target=lambda: serialServer.start())

statemachine = StateMachine(states, remoteValue.getremoteValue(remoteValueType.WorkingMode, remoteValues))
stateMachineThread = threading.Thread(target=lambda: statemachine.start())

udpServerThread.start()
# serialServerThread.start()
stateMachineThread.start()

print("Program started")

def onExit():
    camera.release()
    outputStream.release()
    udpServer.stop()
    # serialServer.stop()

atexit.register(onExit)
