from bot_fsm import *
import pygame
   
class InputManager(BOTFSM):
    
    @staticmethod
    def __runningInit(self):
        self.getFSM().resetInputs()

    @staticmethod
    def __runningTransitionFrom(self, fromState):
        self.getFSM().resetInputs()

    @staticmethod
    def __runningTransitionTo(self, toState):
        self.getFSM().resetInputs()

    @staticmethod
    def __runningUpdate(self, deltaTime):
        self.getFSM().setInputs(pygame.event.get(), pygame.key.get_pressed, pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    @staticmethod
    def __runningLateUpdate(self):
        pass
    
    def resetInputs(self):
        self.keys = {}
        self.events = []
        self.mx, self.my = 0, 0
        self.mouseKeys = []

    def setInputs(self, events, keys, mpos, mkeys):
        self.events = events
        self.keys = keys
        self.mx, self.my = mpos
        self.mouseKeys = mkeys
        
    def getKey(self, key):
        return self.keys[key]
    
    def getMouseCoords(self):
        return (self.mx, self.my)
    
    def getMouseKeys(self, key):
        return self.mouseKeys[key]
    
    def getEvent(self, type):
        for evt in self.events:
            if evt.type == type:
                return evt
        return None
    
            
    


    def init(self):
        states = [
            BOTFSMState(self, "running",
                {
                    "init" : self.__runningInit,
                    "transitionFrom" : self.__runningTransitionFrom,
                    "transitionTo" : self.__runningTransitionTo,
                    "update" : self.__runningUpdate,
                    "lateUpdate" : self.__runningLateUpdate,
                })
            ]
        initState = "running"
        return [initState, states]