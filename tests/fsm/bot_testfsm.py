from bot_framework.bot_fsm import *

class MyContextClass:
    def __init__(self, FSMClass, quack):
        self.quack = quack
        self.fsm = FSMClass(self)

    def duck(self):
        print "\t\t\t\t\t\t\t\t%s" % self.quack

    def update(self, deltaTime):
        self.fsm.update(deltaTime)

    def lateUpdate(self):
        self.fsm.lateUpdate()

class BOTFSMTestClass(BOTFSM):
    # standByState
    @staticmethod
    def __standbyInit(self):
        print "Initializing %s"%(self.getName())
        self.foo = 4
        self.bar = 0

    @staticmethod
    def __standbyTransitionFrom(self, fromState):
        if (fromState == None):
            print "start state %s"%(self.getName())
        else:
            print "transitioning into %s from %s"%(self.getName(), fromState.getName())

    @staticmethod    
    def __standbyTransitionTo(self, toState):
        print "transitioning from %s into %s"%(self.getName(), toState.getName())

    @staticmethod
    def __standbyUpdate(self, deltaTime):
        self.getContext().duck() # use method from context
        print "Updating current state %s, with deltaTime = %.2f"%(self.getName(), deltaTime)
        print "bar = %i"%self.bar
        self.bar += 1
        if self.bar == self.foo:
            self.bar = 0
            self.transitionToState("walking")

    @staticmethod
    def __standbyLateUpdate(self):
        print "LateUpdate of current state %s"%(self.getName())
    
    # walkingState
    @staticmethod
    def __walkingInit(self):
        print "Initializing %s"%(self.getName())
        self.foo = 6
        self.bar = 0

    @staticmethod
    def __walkingTransitionFrom(self, fromState):
        if (fromState == None):
            print "start state %s"%(self.getName())
        else:
            print "transitioning into %s from %s"%(self.getName(), fromState.getName())

    @staticmethod
    def __walkingTransitionTo(self, toState):
        print "transitioning from %s into %s"%(self.getName(), toState.getName())

    @staticmethod
    def __walkingUpdate(self, deltaTime):
        print "Updating current state %s, with deltaTime = %.2f"%(self.getName(), deltaTime)
        print "bar = %i"%self.bar
        self.bar += 1
        if self.bar == self.foo:
            self.bar = 0
            self.transitionToState("standby")

    @staticmethod
    def __walkingLateUpdate(self):
        print "LateUpdate of current state %s"%(self.getName())

    def FSMInit(self):
        states = [
                    {
                        "name" : "standby",
                        "methods" : {
                            "init" : self.__standbyInit,
                            "transitionFrom" : self.__standbyTransitionFrom,
                            "transitionTo" : self.__standbyTransitionTo,
                            "update" : self.__standbyUpdate,
                            "lateUpdate" : self.__standbyLateUpdate
                        }
                    },
                    {
                        "name" : "walking",
                        "methods" : {
                            "init" : self.__walkingInit,
                            "transitionFrom" : self.__walkingTransitionFrom,
                            "transitionTo" : self.__walkingTransitionTo,
                            "update" : self.__walkingUpdate,
                            "lateUpdate" : self.__walkingLateUpdate
                        }
                    }
                ]
        initState = "standby"
        return [initState, states]

def run():
    class_using_fsm = MyContextClass(BOTFSMTestClass, "Quackles!")

    for i in range(20):
        class_using_fsm.update(float(i))
        class_using_fsm.lateUpdate()
