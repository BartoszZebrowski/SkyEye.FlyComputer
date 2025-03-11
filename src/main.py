import threading

from models.remoteVariable import RemoteVariable
from models.remoteVariableType import RemoteVariableType
from tcpServer import TcpServer
from states.followState import FollowState
from states.manualState import ManualState
from states.stateMachine import StateMachine 

remoteVariablesLock = threading.Lock()
remoteVariables = [
    RemoteVariable(RemoteVariableType.HorisonalAxis.value, 0),
    RemoteVariable(RemoteVariableType.VerticalAxis.value, 0),
    RemoteVariable(RemoteVariableType.WorkingMode.value, 0),
]

states = [
    FollowState(),
    ManualState()
]




## zadbac o wielowatkowosc
server = TcpServer(5001, remoteVariables, remoteVariablesLock)
serverThread = threading.Thread(target=lambda: server.start())

statemachine = StateMachine(states)
stateMachineThread = threading.Thread(target=lambda: statemachine.start())

# serialClient = SerialClient

serverThread.start()
stateMachineThread.start()



print("Dziala")