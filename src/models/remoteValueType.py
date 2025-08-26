from enum import Enum

class RemoteVariableType(Enum):
        Ping = 0
        WorkingMode = 1
        TargetHorizontalAngle = 2
        TargetVerticalAngle = 3
        ActualHorizontaAngle = 4
        ActualVerticalAngle = 5
        ZoomValue = 6

class RemoteVariableDevice(Enum):
        PC = 0,
        Arduino = 1,
