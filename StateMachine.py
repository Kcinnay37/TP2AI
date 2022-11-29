from Actor import Actor
from transitions import Machine, State
from transitions.extensions import MachineFactory, GraphMachine

diagram_cls = MachineFactory.get_predefined(graph=True)

class StateMachine(Actor):
    
    machine:Machine
    states = []

    updatesStates = {}
    currentState:str

    def __init__(self, tag:str, type:str):
        super().__init__(tag, type)
        self.states = []
        self.updatesStates = {}
        self.currentState = ""

    def PlayTransition(self, transitionName:str):
        self.trigger(transitionName)

    def AddState(self, name:str, onEnter, onExit, update):
        self.states.append(State(name, onEnter, onExit))
        self.updatesStates[name] = update

    def AddTransition(self, name:str, first:str, last:str, conditions):
        self.machine.add_transition(name, first, last, conditions)

    def InitMachine(self, initialState:str):
        self.currentState = initialState
        self.machine = diagram_cls(model=self, states=self.states, initial=initialState, show_auto_transitions=True, show_conditions=True, show_state_attributes=True)

    def SetCurrentState(self, stateName:str):
        self.currentState = stateName

    def Update(self):
        self.updatesStates[self.currentState]()