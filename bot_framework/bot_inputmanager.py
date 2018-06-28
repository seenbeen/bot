import pygame
from util.bot_math import Vector2
from util.pattern.bot_singleton import Singleton
from util.bot_collections import DictUtil

class InputManager(object):
    def __init__(self):
        self.__inputTree = {}
        self.__priority = []

    def setupPriority(self, listOfPriorities):
        self.__inputTree = {}
        for prio in listOfPriorities:
            self.__inputTree[prio] = []
        self.__priority = listOfPriorities

    def update(self, deltaTime):
        for evt in pygame.event.get():
            self.__propogateEvent(evt)

    def __propogateEvent(self, evt):
        for key in self.__priority:
            for obj in self.__inputTree[key]:
                if obj.sendEvent(evt):
                    return
      
    def _registerListener(self, obj, priority):
        if isinstance(obj, InputListener):
            lst = DictUtil.tryFetch(self.__inputTree, priority, "Priority %s does not exist"%priority)
            lst.append(obj)
        else:
            raise Exception("'%s' is not an input listener and cannot be registered to the input manager"%obj.__class__.__name__)
      
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
                raise Exception("provided object: '%s' is being registered multiple times"%obj.__class__.__name__)
        else:
            raise Exception("provided object: '%s' is not an input listener and cannot be registered to the input manager"%obj.__class__.__name__)

    def registerManager(self, priority):
        if (self._parent == None):
            InputManager.instance()._registerListener(self, priority)
            self._parent = InputManager.instance()
        else:
            raise Exception("'%s' is being registered multiple times"%self.__class__.__name__)

    def sendEvent(self, evt):
        if self.onEvent(evt):
            return True
        for listener in self.__inputTree:
            if listener.onEvent(evt):
                return True
        return False

    def onEvent(self, evt):
        raise Exception("Error, 'onEvent' is not implemented in '%s'."%(self.__class__.__name__))

Singleton.transformToSingleton(InputManager)

