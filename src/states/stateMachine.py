from states.state import State


class StateMachine:
    def __init__(self, states, remoteVariableState):
        self.remoteVariableState = remoteVariableState
        self.states = states

    def start(self):
        while True:
            self.states[0].execute()
