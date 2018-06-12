class BOTFSM:
    def __init__(self, context=None):
        if context == None:
            context = self
        initStateKey, states = self.FSMInit()
        self.__states = {}
        for s in states:
            if s['name'] in self.__states:
                raise Exception('Error, state %s is defined twice when initializing BOTFSM %s.'%(s.getName(), self.__class__.__name__))
            self.__states[s['name']] = _BOTFSMState(self, s['name'], s['methods'], context)
            
        if initStateKey not in self.__states:
            raise Exception('Error, starting state %s is not in %s states [%s]'%(initStateKey, self.__class__.__name__, ", ".join(self.__states.keys())))
        self.__currentState = self.__states[initStateKey]
        self.__transitionToState = None
        self.__currentState.transitionFrom(None)

    """
        init must return a tuple containing a
        the initial state key, and a list of states belonging to the FSM
    """
    def FSMInit(self):
        raise Exception('Error, %s must define BOTFSM initStates'%self.__class__.__name__)

    def transitionToState(self, stateKey):
        if stateKey not in self.__states:
            raise Exception('Error, %s is not in %s states [%s]'%(stateKey, self.__class__.__name__, ", ".join(self.__states.keys())))
        self.__transitionToState = stateKey

    def update(self, deltaTime):
        self.__currentState.update(deltaTime)

    def lateUpdate(self):
        self.__currentState.lateUpdate()
        if self.__transitionToState != None:
            newState = self.__states[self.__transitionToState]
            self.__transitionToState = None
            self.__currentState.transitionTo(newState)
            newState.transitionFrom(self.__currentState)
            self.__currentState = newState
        
class _BOTFSMState:
    """
        meths must be a dict of methods
        which are implementations of the following:
        init(self)
        transitionFrom(self, fromState)
        transitionTo(self, toState)
        update(self, deltaTime)
        lateUpdate(self)
    """
    def __init__(self, fsm, name, meths, context):
        self.__fsm = fsm
        self.__name = name
        meths["init"](self)
        self.__transitionFrom = meths["transitionFrom"]
        self.__transitionTo = meths["transitionTo"]
        self.__update = meths["update"]
        self.__lateUpdate = meths["lateUpdate"]
        self.__context = context

    def getName(self):
        return self.__name

    def transitionFrom(self, fromState):
        self.__transitionFrom(self, fromState)

    def transitionTo(self, toState):
        self.__transitionTo(self, toState)

    def update(self, deltaTime):
        self.__update(self, deltaTime)

    def lateUpdate(self):
        self.__lateUpdate(self)

    def transitionToState(self, stateKey):
        self.__fsm.transitionToState(stateKey)

    def getContext(self):
        return self.__context
