import serial


class SerialServer:

    def __init__(self, portCom, baudrate, timeout, remoteVariables, remoteVariablesLock):
        self.remoteVariables = remoteVariables
        self.remoteVariablesLock = remoteVariablesLock 
        self.serial = []

        self.serial = serial.Serial(
            port=portCom,
            baudrate=baudrate,
            timeout=timeout
        )

    def start(self):
        while True:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('utf-8').rstrip()
                response = self.handeMessage(line)

                print(f"[ARDUINO]: {response}")
                                
                self.serial.write(response.encode())


    def stop(self):
        self.serial.close()


    def handeMessage(self, data):
        if data.count(";") != 2:
            print(f"[ARDUINO]: {data}")
            return f"0;0"

        splitedData = data.split(";")

        remoteVariableType = int(splitedData[0])
        remoteVariableMode= int(splitedData[1])
        remoteVariableContent = float(splitedData[2])

        if remoteVariableType is None or remoteVariableMode is None or remoteVariableContent is None :
            raise NameError("Wrong data")

        remoteVariable = next((x for x in self.remoteVariables if x.remoteVariableType.value == remoteVariableType),None)

        if remoteVariable is None:
            raise NameError("This remote variable dont exist")
        
        if remoteVariableMode == 1:
            with self.remoteVariablesLock:
                remoteVariable.set(remoteVariableContent)
                print(f"Zwrocono {remoteVariableContent}")

        value = str(remoteVariable.get())
        

        return f"{remoteVariableType};{value}".replace(".", ",")