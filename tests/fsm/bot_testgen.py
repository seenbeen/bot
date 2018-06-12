from bot_framework.bot_fsm import *

class BOTTestGen(BOTFSM):
    # start_state
    @staticmethod
    def __start_stateInit(self):
        print "Initializing %s"%(self.getName())
        self.foo = 2
        self.bar = 0

    @staticmethod
    def __start_stateTransitionFrom(self, fromState):
        if (fromState == None):
            print "start state %s"%(self.getName())
        else:
            print "transitioning into %s from %s"%(self.getName(), fromState.getName())

    @staticmethod
    def __start_stateTransitionTo(self, toState):
        print "transitioning from %s into %s"%(self.getName(), toState.getName())

    @staticmethod
    def __start_stateUpdate(self, deltaTime):
        print "Updating current state %s, with deltaTime = %.2f"%(self.getName(), deltaTime)
        print "bar = %i"%self.bar
        self.bar += 1
        if self.bar == self.foo:
            self.bar = 0
            self.transitionToState("mid_state")

    @staticmethod
    def __start_stateLateUpdate(self):
        print "LateUpdate of current state %s"%(self.getName())


    # mid_state
    @staticmethod
    def __mid_stateInit(self):
        print "Initializing %s"%(self.getName())
        self.foo = 3
        self.bar = 0

    @staticmethod
    def __mid_stateTransitionFrom(self, fromState):
        if (fromState == None):
            print "start state %s"%(self.getName())
        else:
            print "transitioning into %s from %s"%(self.getName(), fromState.getName())

    @staticmethod
    def __mid_stateTransitionTo(self, toState):
        print "transitioning from %s into %s"%(self.getName(), toState.getName())

    @staticmethod
    def __mid_stateUpdate(self, deltaTime):
        print "Updating current state %s, with deltaTime = %.2f"%(self.getName(), deltaTime)
        print "bar = %i"%self.bar
        self.bar += 1
        if self.bar == self.foo:
            self.bar = 0
            self.transitionToState("end_state")

    @staticmethod
    def __mid_stateLateUpdate(self):
        print "LateUpdate of current state %s"%(self.getName())


    # end_state
    @staticmethod
    def __end_stateInit(self):
        print "Initializing %s"%(self.getName())
        self.foo = 5
        self.bar = 0

    @staticmethod
    def __end_stateTransitionFrom(self, fromState):
        if (fromState == None):
            print "start state %s"%(self.getName())
        else:
            print "transitioning into %s from %s"%(self.getName(), fromState.getName())

    @staticmethod
    def __end_stateTransitionTo(self, toState):
        print "transitioning from %s into %s"%(self.getName(), toState.getName())

    @staticmethod
    def __end_stateUpdate(self, deltaTime):
        print "Updating current state %s, with deltaTime = %.2f"%(self.getName(), deltaTime)
        print "bar = %i"%self.bar
        self.bar += 1
        if self.bar == self.foo:
            self.bar = 0
            self.transitionToState("start_state")

    @staticmethod
    def __end_stateLateUpdate(self):
        print "LateUpdate of current state %s"%(self.getName())

    def FSMInit(self):
        states = [
                    {
                        "name" : "start_state",
                        "methods" : {
                            "init" : self.__start_stateInit,
                            "transitionFrom" : self.__start_stateTransitionFrom,
                            "transitionTo" : self.__start_stateTransitionTo,
                            "update" : self.__start_stateUpdate,
                            "lateUpdate" : self.__start_stateLateUpdate,
                        }
                    },
                    {
                        "name" : "mid_state",
                        "methods" : {
                            "init" : self.__mid_stateInit,
                            "transitionFrom" : self.__mid_stateTransitionFrom,
                            "transitionTo" : self.__mid_stateTransitionTo,
                            "update" : self.__mid_stateUpdate,
                            "lateUpdate" : self.__mid_stateLateUpdate,
                        }
                    },
                    {
                        "name" : "end_state",
                        "methods" : {
                            "init" : self.__end_stateInit,
                            "transitionFrom" : self.__end_stateTransitionFrom,
                            "transitionTo" : self.__end_stateTransitionTo,
                            "update" : self.__end_stateUpdate,
                            "lateUpdate" : self.__end_stateLateUpdate,
                        }
                    }
                ]
        initState = "start_state"
        return [initState, states]

def run():
    myFSM = BOTTestGen()

    for i in range(20):
        myFSM.update(float(i))
        myFSM.lateUpdate()
