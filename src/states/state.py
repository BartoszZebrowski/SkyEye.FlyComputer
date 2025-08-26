## @class State
#  @brief Klasa bazowa dla wszystkich stanów w maszynie stanów.
class State:
    
    ## @brief Metoda abstrakcyjna do implementacji logiki stanu.
    #  @exception NotImplementedError Jeśli metoda nie została nadpisana w klasie pochodnej.
    def execute(self):
        raise NotImplementedError()