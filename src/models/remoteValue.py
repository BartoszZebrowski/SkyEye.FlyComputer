## @class RemoteValue
#  @brief Klasa przechowująca zdalną wartość wraz z jej typem.
class RemoteValue():

    ## @brief Konstruktor klasy RemoteValue.
    #  @param remoteValueType Typ zdalnej wartości.
    #  @param initValue Wartość początkowa.
    def __init__(self, remoteValueType, initValue):
        self.remoteValueType = remoteValueType
        self.value = initValue

    ## @brief Ustawia nową wartość.
    #  @param value Nowa wartość do zapisania.
    def set(self, value):
        self.value = value

    ## @brief Zwraca aktualnie zapisaną wartość.
    #  @return Bieżąca wartość.
    def get(self):
        return self.value
    
    ## @brief Wyszukuje obiekt RemoteValue o podanym typie w liście.
    #  @param type Typ poszukiwanej wartości.
    #  @param remoteValues Lista obiektów RemoteValue.
    #  @return Obiekt RemoteValue o danym typie lub None, jeśli nie znaleziono.
    def getRemoteValue(type, remoteValues):
        return next((x for x in remoteValues if x.remoteValueType == type), None)
