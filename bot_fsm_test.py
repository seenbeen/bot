from bot_fsm import *

class BOTFSMTestClass(BOTFSM):
    # standByState
    @staticmethod
    def __standbyInit(self):
        print "Initializing %s"%(self.name)
        self.foo = 4
        self.bar = 0

    @staticmethod
    def __standbyTransitionFrom(self, fromState):
        print "transitioning into %s from %s"%(self.name, fromState.name)

    @staticmethod    
    def __standbyTransitionTo(self, toState):
        print "transitioning from %s into %s"%(self.name, toState.name)

    @staticmethod
    def __standbyUpdate(self, deltaTime):
        print "Updating current state %s, with deltaTime = %.2f"%(self.name, deltaTime)
        print "bar = %i"%self.bar
        self.bar += 1
        if self.bar == self.foo:
            self.bar = 0
            self.transitionToState("walking")

    @staticmethod
    def __standbyLateUpdate(self):
        print "LateUpdate of current state %s"%(self.name)
    
    # walkingState
    @staticmethod
    def __walkingInit(self):
        print "Initializing %s"%(self.name)
        self.foo = 6
        self.bar = 0

    @staticmethod
    def __walkingTransitionFrom(self, fromState):
        print "transitioning into %s from %s"%(self.name, fromState.name)

    @staticmethod
    def __walkingTransitionTo(self, toState):
        print "transitioning from %s into %s"%(self.name, toState.name)

    @staticmethod
    def __walkingUpdate(self, deltaTime):
        print "Updating current state %s, with deltaTime = %.2f"%(self.name, deltaTime)
        print "bar = %i"%self.bar
        self.bar += 1
        if self.bar == self.foo:
            self.bar = 0
            self.transitionToState("standby")

    @staticmethod
    def __walkingLateUpdate(self):
        print "LateUpdate of current state %s"%(self.name)

    def init(self):
        states = [
            BOTFSMState("standby",
                {
                    "init" : self.__standbyInit,
                    "transitionFrom" : self.__standbyTransitionFrom,
                    "transitionTo" : self.__standbyTransitionTo,
                    "update" : self.__standbyUpdate,
                    "lateUpdate" : self.__standbyLateUpdate
                }),
            BOTFSMState("walking",
                {
                    "init" : self.__walkingInit,
                    "transitionFrom" : self.__walkingTransitionFrom,
                    "transitionTo" : self.__walkingTransitionTo,
                    "update" : self.__walkingUpdate,
                    "lateUpdate" : self.__walkingLateUpdate
                })
            ]
        initState = "standby"
        return [initState, states]

myFSM = BOTFSMTestClass()

for i in range(20):
    myFSM.update(float(i))
    myFSM.lateUpdate()
