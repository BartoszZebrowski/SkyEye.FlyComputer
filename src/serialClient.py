import serial


class SerialClient:

    def __init__(self, portCom, baudrate, timeout):

        self.serial = []

        # self.serial = serial.Serial(
        #     port=portCom,
        #     baudrate=baudrate,
        #     timeout=timeout
        # )

    def getValue(self, valueType):
        self.serial.write(f"{valueType}:0:0")
        received_data = self.serial.readline().decode('utf-8').strip()
        self.serial.close()
        return received_data

    def setValue(self, valueType, value):
        self.serial.write(f"{valueType}:1:{value}")
        received_data = self.serial.readline().decode('utf-8').strip()
        self.serial.close()
        return received_data
