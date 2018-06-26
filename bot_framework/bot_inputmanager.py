import pygame
from bot_fsm import *
from util.bot_math import Vector2
from util.pattern.bot_singleton import Singleton

class InputManager(BOTFSM):
    KEYS = 0
    EVENTS = 1
    MOUSEPOS = 2
    MOUSEBUTTONS = 3

    # running
    @staticmethod
    def __runningInit(self):
        self.getContext().resetInputs()

    @staticmethod
    def __runningTransitionFrom(self, fromState):
        self.getContext().resetInputs()

    @staticmethod
    def __runningTransitionTo(self, toState):
        self.getContext().resetInputs()

    @staticmethod
    def __runningUpdate(self, deltaTime):
        self.getContext().setInputs(pygame.event.get(), InputManager.EVENTS)
        self.getContext().setInputs(pygame.key.get_pressed(), InputManager.KEYS)
        self.getContext().setInputs(pygame.mouse.get_pos(), InputManager.MOUSEPOS)
        self.getContext().setInputs(pygame.mouse.get_pressed(), InputManager.MOUSEBUTTONS)

    @staticmethod
    def __runningLateUpdate(self):
        pass
    
    def resetInputs(self):
        self.keys = {}
        self.events = []
        self.mx, self.my = 0, 0
        self.mouseKeys = []

    def setInputs(self, inputData, dataType):
        if (dataType == InputManager.KEYS):
            self.keys = inputData
        elif (dataType == InputManager.EVENTS):
            self.events = inputData
        elif (dataType == InputManager.MOUSEPOS):
            self.mx, self.my = inputData
        elif (dataType == InputManager.MOUSEBUTTONS):
            self.mouseButtons = inputData
        else:
            raise Exception("Invalid type of input data was submitted to the input manager")
        
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
    
    def FSMInit(self):
        states = [
                    {
                        "name" : "running",
                        "methods" : {
                            "init" : self.__runningInit,
                            "transitionFrom" : self.__runningTransitionFrom,
                            "transitionTo" : self.__runningTransitionTo,
                            "update" : self.__runningUpdate,
                            "lateUpdate" : self.__runningLateUpdate,
                        }
                    }
                ]
        initState = "running"
        return [initState, states]
    
Singleton.transformToSingleton(InputManager)
