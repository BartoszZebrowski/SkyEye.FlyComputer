from states.state import State


## @class StateMachine
#  @brief Klasa implementująca maszynę stanów sterującą logiką programu.
class StateMachine:

    
    ## @brief Konstruktor maszyny stanów.
    #  @param states Lista obiektów stanów.
    #  @param remoteValuesState Obiekt RemoteValue określający aktualny stan.
    def __init__(self, states, remoteValuesState):
        self.remoteValuesState = remoteValuesState
        self.states = states
        print(remoteValuesState)

    ## @brief Uruchamia maszynę stanów i wykonuje logikę aktualnego stanu w pętli.
    def start(self):
        while True:
            self.states[int(self.remoteValuesState.get())].execute()
            pass

