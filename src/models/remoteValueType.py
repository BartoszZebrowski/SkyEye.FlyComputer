from enum import Enum

## @enum RemoteValueType
#  @brief Typy zdalnych wartości przesyłanych między urządzeniami.
class RemoteValueType(Enum):
        Ping = 0
        WorkingMode = 1
        TargetHorizontalAngle = 2
        TargetVerticalAngle = 3
        ActualHorizontaAngle = 4
        ActualVerticalAngle = 5
        ZoomValue = 6

## @enum RemoteValueDevice
#  @brief Typy urządzeń wymieniających dane.
class RemoteValueDevice(Enum):
        PC = 0,
        Arduino = 1,
