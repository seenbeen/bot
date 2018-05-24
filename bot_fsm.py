class BOTFSM: # extends BOTGameObjectComponent
    def __init__(self):
        initStateKey, states = self.init()
        self.__states = {}
        for s in states:
            if s.name in self.__states:
                raise Exception('Error, state %s is defined twice when initializing BOTFSM %s.'%self.__class__.__name__)
            s.fsm = self
            self.__states[s.name] = s
            
        if initStateKey not in self.__states:
            raise Exception('Error, starting state %s is not in %s states [%s]'%(initStateKey, self.__class__.__name__, ", ".join(self.__states.keys())))
        self.__currentState = self.__states[initStateKey]
        self.__transitionToState = None

    """
        init must return a tuple containing a
        the initial state key, and a list of states belonging to the FSM
    """
    def init(self):
        raise Exception('Error, %s must define BOTFSM initStates'%self.__class__.__name__)

    def transitionTo(self, stateKey):
        if stateKey not in self.__states:
            raise Exception('Error, %s is not in %s states [%s]'%(stateKey, self.__class__.__name__, ", ".join(self.__states.keys())))
        self.__transitionToState = stateKey

    def update(self, deltaTime):
        self.__currentState.update(self.__currentState, deltaTime)

    def lateUpdate(self):
        self.__currentState.lateUpdate(self.__currentState)
        if self.__transitionToState != None:
            newState = self.__states[self.__transitionToState]
            self.__transitionToState = None
            self.__currentState.transitionTo(self.__currentState, newState)
            newState.transitionFrom(newState, self.__currentState)
            self.__currentState = newState
        
class BOTFSMState:
    """
        meths must be a dict of methods
        which are implementations of the following:
        init(self)
        transitionFrom(self, fromState)
        transitionTo(self, toState)
        update(self, deltaTime)
        lateUpdate(self)
    """
    def __init__(self, name, meths):
        self.fsm = None
        self.name = name
        meths["init"](self)
        self.transitionFrom = meths["transitionFrom"]
        self.transitionTo = meths["transitionTo"]
        self.update = meths["update"]
        self.lateUpdate = meths["lateUpdate"]

    def transitionToState(self, stateKey):
        if self.fsm == None:
            raise Exception('Error, please do NOT try to transition to states in FSMState init from $s'%(self.__class__.__name__))
        self.fsm.transitionTo(stateKey)
