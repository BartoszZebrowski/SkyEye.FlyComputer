import socket
import threading

class UdpServer:
    
    def __init__(self, port, remoteVariables, remoteVariablesLock):
        self.port = port
        self.adress = "0.0.0.0" 
        self.remoteVariables = remoteVariables
        self.remoteVariablesLock = remoteVariablesLock


    def start(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((self.adress, self.port))

        print(f"Serwer nasłuchuje na {self.adress}:{self.port}")

        while True:
            try:
                data, client_address = self.serverSocket.recvfrom(1024)
                message = data.decode()
                # print(f"Otrzymano od {client_address}: {message}")
                
                response = self.handeMessage(message)        

                self.serverSocket.sendto(response.encode(), client_address)

            except Exception as e:
                print(f"Zdarzył się błąd: {e}")

    def stop(self):
        self.serverSocket.close()
        print("Zamknieto socket")

    def handeMessage(self, data):
        splitedData = data.split(";")
        remoteVariableType = int(splitedData[0])
        remoteVariableMode= int(splitedData[1])
        remoteVariableContent = float(splitedData[2])

        if remoteVariableType is None or remoteVariableMode is None or remoteVariableContent is None :
            raise NameError("Wrong data")
        
        remoteVariable = next((x for x in self.remoteVariables if x.remoteVariableType.value[0] == remoteVariableType),None)

        if remoteVariable is None:
            raise NameError("This remote variable dont exist")
        
        if remoteVariableMode == 1:
            with self.remoteVariablesLock:
                remoteVariable.set(remoteVariableContent)
                print(f"Zwrocono {remoteVariableContent}")

        value = str(remoteVariable.get())

        return f"{remoteVariableType};{value}"




