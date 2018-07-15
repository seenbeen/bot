import pygame
from util.bot_math import Vector2
from util.pattern.bot_singleton import Singleton
from util.bot_collections import DictUtil

class InputManager(object):
    def __init__(self):
        self.__nodes = {}
        self.__priority = []
        self.__IDmap = {}
        self.__IDCount = 0

    def sendEvent(self, evt):
        for key in self.__priority:
            for obj in self.__nodes[key]:
                if obj.sendEvent(evt):
                    return

    def _addListener(self, listener, parent):
        for obj in self.__IDmap:
            if (obj == listener):
                raise Exception("Error, %s object is already in the input tree"%listener.__class__.__name__)
        if (isinstance(listener, InputListener)):
            temp = InputTreeNode(self.__IDCount, listener)
            self.__IDmap[self.__IDCount] = temp
            self.__IDCount += 1
            
            if (isinstance(parent, int)):
                self.__IDmap[parent].addNode(temp)
                temp._parentNode = self.__IDmap[parent]
            elif (isinstance(parent, InputListener)):
                self.__IDmap[parent.ID].addNode(temp)
                temp._parentNode = self.__IDmap[parent.ID]
            else:
                raise Exception("provided object: '%s' is not a correct parent input type and cannot be registered to the input manager"%parent.__class__.__name__)
                
        else:
            raise Exception("provided object: '%s' is not an input listener and cannot be registered to the input manager"%listener.__class__.__name__)
    
    def setupPriority(self, listOfPriorities):
        for i in listOfPriorities:
            if not (isinstance(i,int)):
                raise Exception("Error, Input Priorities MUST be integers")
        self.__nodes = {}
        for prio in listOfPriorities:
            self.__nodes[prio] = InputTreeNode(self.__IDCount, None)
            self.__nodes[prio]._parentNode = self
            self.__IDmap[self.__IDCount] = self.__nodes[prio]
            self.__IDCount += 1
            
        self.__priority = listOfPriorities[:]

    def update(self, deltaTime):
        for evt in pygame.event.get():
            self.__propogateEvent(evt)

    def __propogateEvent(self, evt):
        for key in self.__priority:
            if self.__nodes[key].sendEvent(evt):
                return
        
    def lateUpdate(self):
        pass

class InputListener(object):
    def addListener(self, obj):
        InputManager.instance()._addListener(obj, self.treeNode.ID)

    def registerToManager(self, priority):
        InputManager.instance()._addListener(self, priority)
    
    def bringFocus(self):
        self.treeNode.bringFocus(self)

    def onEvent(self, evt):
        raise Exception("Error, 'onEvent' is not implemented in '%s'."%(self.__class__.__name__))

class InputTreeNode(object):
    def __init__(self, ID, obj):
        self.ID = ID
        self.__nodes = []
        self._parentNode = None
        self.setObj(obj)
    
    def setObj(self, listener):
        if (isinstance(listener, InputListener)):
            self.obj = listener
            listener.ID = self.ID
            listener.treeNode = self
        elif listener is None:
            self.obj = None
        else:
            raise Exception("Error, %s is not an inputListener being added to the tree"%listener.__class__.__name__)
        
    def addNode(self, node):
        if (isinstance(node,InputTreeNode)):
            self.__nodes.append(node)
            node._parentNode = self
        else:
            raise Exception("Error, %s is not an inputTreeNode being added to the tree"%node.__class__.__name__)
    
    def sendEvent(self, evt):
        if self.obj != None:
            if (self.obj.onEvent(evt)):
                return True
        for node in self.__nodes:
            if (node.sendEvent(evt)):
                return True
        return False
    
    def bringFocus(self, listener):
        if listener in self.__inputTree:
            temp = self.__inputTree.pop(self.__inputTree.index(listener))
            self.inputTree.insert(0, temp)
        
Singleton.transformToSingleton(InputManager)
        