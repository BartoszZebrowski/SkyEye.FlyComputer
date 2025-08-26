from states.state import State


class StateMachine:
    def __init__(self, states, remoteValuesState):
        self.remoteValuesState = remoteValuesState
        self.states = states
        print(remoteValuesState)

    def start(self):
        while True:
            self.states[int(self.remoteValuesState.get())].execute()
            pass

