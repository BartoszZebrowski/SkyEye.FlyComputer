import serial


## @class SerialServer
#  @brief Serwer komunikacji szeregowej obsługujący wymianę danych z Arduino.
class SerialServer:

    ## @brief Inicjalizuje serwer portu szeregowego i referencje do zdalnych wartości.
    #  @param portCom Nazwa portu szeregowego (np. "COM3" lub "/dev/ttyUSB0").
    #  @param baudrate Prędkość transmisji (baud).
    #  @param timeout Timeout odczytu z portu (sekundy).
    #  @param remoteValues Lista obiektów RemoteValue przechowujących wartości zdalne.
    #  @param remoteValuesLock Blokada (mutex) do bezpiecznej współbieżnej modyfikacji remoteValues.
    def __init__(self, portCom, baudrate, timeout, remoteValues, remoteValuesLock):
        self.remoteValues = remoteValues
        self.remoteValuesLock = remoteValuesLock 
        self.serial = []

        self.serial = serial.Serial(
            port=portCom,
            baudrate=baudrate,
            timeout=timeout
        )

    ## @brief Uruchamia główną pętlę serwera: czyta linie z portu, przetwarza i odsyła odpowiedzi.
    def start(self):
        while True:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('utf-8').rstrip()
                response = self.handeMessage(line)

                print(f"[ARDUINO]: {response}")
                                
                self.serial.write(response.encode())


    ## @brief Zamyka połączenie szeregowe.
    def stop(self):
        self.serial.close()


    ## @brief Przetwarza pojedynczą wiadomość w formacie „typ;tryb;wartość”.
    #  @param data Linia tekstu odebrana z portu szeregowego.
    #  @return Odpowiedź w formacie „typ;wartość” (z przecinkiem jako separatorem dziesiętnym).
    #  @exception NameError Gdy dane są niepoprawne lub wskazana zmienna zdalna nie istnieje.
    def handeMessage(self, data):
        if data.count(";") != 2:
            print(f"[ARDUINO]: {data}")
            return f"0;0"

        splitedData = data.split(";")

        remoteValueType = int(splitedData[0])
        remoteValueMode= int(splitedData[1])
        remoteValueContent = float(splitedData[2])

        if remoteValueType is None or remoteValueMode is None or remoteValueContent is None :
            raise NameError("Wrong data")

        remoteValue = next((x for x in self.remoteValues if x.remoteValueType.value == remoteValueType),None)

        if remoteValue is None:
            raise NameError("This remote variable dont exist")
        
        if remoteValueMode == 1:
            with self.remoteValuesLock:
                remoteValue.set(remoteValueContent)
                print(f"Zwrocono {remoteValueContent}")

        value = str(remoteValue.get())
        

        return f"{remoteValueType};{value}".replace(".", ",")