import pygame
from util.bot_math import Vector2
from util.pattern.bot_singleton import Singleton

class InputManager(object):
    
    def __init__(self):
        self.__inputTree = {}

    def update(self, deltaTime):
        for evt in pygame.event.get():
            self.propogateEvent(evt)

    def propogateEvent(self, evt):
        for i in range(len(self.__inputTree)):
            for obj in self.__inputTree[i]:
                if obj.sendEvent(evt):
                    return
                
    def registerListener(self, obj, priority):
        if isinstance(obj, InputListener):
            if priority in self.__inputTree:
                self.__inputTree[priority].append(obj)
            else:
                self.__inputTree[priority] = [obj]
                
    def lateUpdate(self):
        pass

class InputListener(object):
    def __init__(self):
        self.__inputTree = []
    
    def addListener(self, obj):
        self.__inputTree.append(obj)
        
    def registerManager(self, priority):
        InputManager.instance().registerListener(self, priority)
    
    def sendEvent(self, evt):
        if self.eventImpl(evt):
            return True
        else:
            for listener in self.__inputTree:
                if listener.sendEvent(evt):
                    return True
        return False
        
    def eventImpl(self, evt):
        raise Exception('Error, eventImpl is not implemented in %s.'%(self.__class__.__name__))
        
Singleton.transformToSingleton(InputManager)
