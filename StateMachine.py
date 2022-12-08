from Actor import Actor
from transitions import Machine, State
from transitions.extensions import MachineFactory, GraphMachine

diagram_cls = MachineFactory.get_predefined(graph=True)

class StateMachine(Actor):
    
    machine:Machine
    states = []

    updatesStates = {}
    currentState:str
    colliderState = {}

    def __init__(self, tag:str, type:str):
        super().__init__(tag, type)
        self.states = []
        self.updatesStates = {}
        self.currentState = ""
        self.colliderState = {}

    # fait jouer une transition
    def PlayTransition(self, transitionName:str):
        self.trigger(transitionName)

    # ajoute une state a la state machien
    def AddState(self, name:str, onEnter, onExit, update, onCollider):
        self.states.append(State(name, onEnter, onExit))
        self.updatesStates[name] = update
        self.colliderState[name] = onCollider

    # ajoute une transition entre deux state
    def AddTransition(self, name:str, first:str, last:str, conditions):
        self.machine.add_transition(name, first, last, conditions)

    # initialise la machine
    def InitMachine(self, initialState:str):
        self.currentState = initialState
        self.machine = diagram_cls(model=self, states=self.states, initial=initialState, show_auto_transitions=True, show_conditions=True, show_state_attributes=True)

    # set la state courrant  pour la garde en mémoir
    def SetCurrentState(self, stateName:str):
        self.currentState = stateName

    # appel le update de la state courrant
    def Update(self):
        self.updatesStates[self.currentState]()

    # appel le OnColldier de la state courrant
    def OnColliderEnter(self, dir):
        self.colliderState[self.currentState](dir)