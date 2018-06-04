from bot_fsm import *
from util.bot_math import Vector2
import pygame
   
class InputManager(BOTFSM):
    __instance = None
    
    KEYS = 0
    EVENTS = 1
    MOUSEPOS = 2
    MOUSEBUTTONS = 3
    
    @staticmethod
    def getInstance():
        if (InputManager.__instance == None):
            InputManager.__instance = InputManager()
        return InputManager.__instance
            
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
        self.getFSM().setInputs(pygame.event.get(), InputManager.EVENTS)
        self.getFSM().setInputs(pygame.key.get_pressed(), InputManager.KEYS)
        self.getFSM().setInputs(pygame.mouse.get_pos(), InputManager.MOUSEPOS)
        self.getFSM().setInputs(pygame.mouse.get_pressed(), InputManager.MOUSEBUTTONS)

    @staticmethod
    def __runningLateUpdate(self):
        pass
    
    def resetInputs(self):
        self.keys = {}
        self.events = []
        self.mx, self.my = 0, 0
        self.mouseKeys = []

    def setInputs(self, set, name):
        if (name == InputManager.KEYS):
            self.keys = set
        elif (name == InputManager.EVENTS):
            self.events = set
        elif (name == InputManager.MOUSEPOS):
            self.mx, self.my = set
        elif (name == InputManager.MOUSEBUTTONS):
            self.mouseButtons = set
        
    def getKeyDown(self, key):
        return self.keys[key]
    
    def getMouseCoords(self):
        return Vector2(self.mx, self.my)
    
    def getMouseButton(self, key):
        return self.mouseButtons[key]
    
    def getEvent(self, type):
        events = []
        for evt in self.events:
            if evt.type == type:
                events.append(evt)
        return events
    
            
    
    

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