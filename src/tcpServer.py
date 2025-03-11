import socket
import threading

class TcpServer:
    
    def __init__(self, port, remoteVariables, remoteVariablesLock):
        self.port = port
        self.adress = "0.0.0.0" 
        self.remoteVariables = remoteVariables
        self.remoteVariablesLock = remoteVariablesLock


    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.adress, self.port))
        server_socket.listen(1)

        print(f"Serwer nasłuchuje na {self.adress}:{self.port}")

        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Połączono z: {addr}")

                while True:
                    data = client_socket.recv(1024).decode()
                    
                    if not data:
                        # Jeśli brak danych, kończymy połączenie
                        break

                    print(f"Otrzymano: {data}")

                    response = self.handeMassage(data)

                    client_socket.send(str(response).encode())

                # Po zakończeniu wymiany danych z klientem, zamykamy połączenie
                client_socket.close()

            except Exception as e:
                print(f"Zdarzył się błąd: {e}")

            

    def handeMassage(self, data):
        splitedData = data.split(";")
        remoteVariableType = int(splitedData[0])
        remoteVariableMode= int(splitedData[1])
        remoteVariableContent = int(splitedData[2])

        if remoteVariableType is None or remoteVariableMode is None or remoteVariableContent is None :
            raise NameError("Wrong data")

        remoteVariable = next((x for x in self.remoteVariables if x.remoteVariableType == remoteVariableType),None)

        if remoteVariable is None:
            raise NameError("This remote variable dont exist")
        
        if remoteVariableMode == 1:
            with self.remoteVariablesLock:
                remoteVariable.set(remoteVariableContent)

        return remoteVariableContent.get()




