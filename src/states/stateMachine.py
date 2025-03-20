from states.state import State


class StateMachine:
    def __init__(self, states, remoteVariableState):
        self.remoteVariableState = remoteVariableState
        self.states = states
        print(remoteVariableState)

    def start(self):
        while True:
            self.states[int(self.remoteVariableState.get())].execute()
            pass

