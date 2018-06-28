import pygame
from util.bot_math import Vector2
from util.pattern.bot_singleton import Singleton
from util.bot_collections import DictUtil

class InputManager(object):
    UI = 0
    MENU = 1
    GAMEOBJECT = 2
    
    def __init__(self):
        self.__inputTree = {}

    def setupPriority(self, list):
        self.__inputTree = {}
        for prio in list:
            self.__inputTree[prio] = []

    def update(self, deltaTime):
        for evt in pygame.event.get():
            self.propogateEvent(evt)

    def propogateEvent(self, evt):
        for key in self.__inputTree:
            for obj in self.__inputTree[key]:
                if obj.sendEvent(evt):
                    return
      
    def registerListener(self, obj, priority):
        if isinstance(obj, InputListener):
            DictUtil.tryFetch(self.__inputTree, priority, "Priority %s does not exist"%priority).append(obj)
        else:
            raise Exception("%s is not an input listener and cannot be registered to the input manager"%obj.__name__)
      
    def lateUpdate(self):
        pass

class InputListener(object):
    def __init__(self):
        self.__inputTree = []
        self._parent = None

    def addListener(self, obj):
        if isinstance(obj, InputListener):
            if (obj._parent == None):
                self.__inputTree.append(obj)
                obj._parent = self
            else:
                raise Exception("%s is being registered multiple times"%obj.__class__.__name__)
        else:
            raise Exception("%s is not an input listener and cannot be registered to the input manager"%obj.__class__.__name__)

    def registerManager(self, priority):
        InputManager.instance().registerListener(self, priority)

    def sendEvent(self, evt):
        if self.onEvent(evt):
            return True
        for listener in self.__inputTree:
            if listener.onEvent(evt):
                return True
        return False

    def onEvent(self, evt):
        raise Exception("Error, 'onEvent' is not implemented in %s."%(self.__class__.__name__))

Singleton.transformToSingleton(InputManager)

