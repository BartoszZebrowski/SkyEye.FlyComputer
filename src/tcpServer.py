import socket
import threading

class TcpServer:
    
    def __init__(self, port, remoteVariables, remoteVariablesLock):
        self.port = port
        self.adress = "0.0.0.0" 
        self.remoteVariables = remoteVariables
        self.remoteVariablesLock = remoteVariablesLock


    def start(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.adress, self.port))
        self.serverSocket.listen(1)

        print(f"Serwer nasłuchuje na {self.adress}:{self.port}")

        while True:
            try:
                clientSocket, addr = self.serverSocket.accept()
                print(f"Połączono z: {addr}")

                while True:
                    data = clientSocket.recv(1024).decode()
                    
                    if not data:
                        # Jeśli brak danych, kończymy połączenie
                        break

                    print(f"Otrzymano: {data}")
                    response = self.handeMessage(data)
                    clientSocket.send(str(response).encode())
                    print(f"Zwrocono: {response}")


                # Po zakończeniu wymiany danych z klientem, zamykamy połączenie
                clientSocket.close()

            except Exception as e:
                print(f"Zdarzył się błąd: {e}")

    def stop(self):
        self.serverSocket.close()
        print("Zamknieto socket")

    def handeMessage(self, data):
        splitedData = data.split(";")
        remoteVariableType = int(splitedData[0])
        remoteVariableMode= int(splitedData[1])
        remoteVariableContent = int(splitedData[2])

        if remoteVariableType is None or remoteVariableMode is None or remoteVariableContent is None :
            raise NameError("Wrong data")
        
        remoteVariable = next((x for x in self.remoteVariables if x.remoteVariableType.value[0] == remoteVariableType),None)

        if remoteVariable is None:
            raise NameError("This remote variable dont exist")
        
        if remoteVariableMode == 1:
            with self.remoteVariablesLock:
                remoteVariable.set(remoteVariableContent)
                print(f"Ustawiono {remoteVariableContent}")

        return remoteVariable.get()




