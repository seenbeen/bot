import pygame
from util.bot_math import Vector2
from util.pattern.bot_singleton import Singleton
from util.bot_collections import DictUtil

class InputManager(object):
    def __init__(self):
        self.__nodes = {}
        self.__priority = []
        self.__IDmap = {}

    def sendEvent(self, evt):
        for key in self.__priority:
            for obj in self.__nodes[key]:
                if obj.sendEvent(evt):
                    return

    '''
    Listeners can be passed in by reference
    Parents can be passed in by reference or by ID
    In both cases, the InputManager will set Listener to be a child of Parent
    '''
    def _addListener(self, listener, parent):
        for key in self.__IDmap:
            if (key == listener.getID()):
                raise Exception("Error, %s object is already in the input tree"%listener.__class__.__name__)
        if (isinstance(listener, InputListener)):
            temp = InputTreeNode(listener)
            self.__IDmap[listener.getID()] = temp
            
            if (isinstance(parent, int) or isinstance(parent, str)):
                DictUtil.tryFetch(self.__IDmap, parent.getID(), "Provided object: '%s' has not been added to the input tree"%parent.__class__.__name__).addNode(temp)
                temp._parentNode = self.__IDmap[parent]
            elif (isinstance(parent, InputListener)):
                DictUtil.tryFetch(self.__IDmap, parent.getID(), "Provided object: '%s' has not been added to the input tree"%parent.__class__.__name__).addNode(temp)
                temp._parentNode = self._getNodeFromListener(parent)
            else:
                raise Exception("provided object: '%s' is not a correct parent input type and cannot be registered to the input manager"%parent.__class__.__name__)
                
        else:
            raise Exception("provided object: '%s' is not an input listener and cannot be registered to the input manager"%listener.__class__.__name__)
        
    def _addToTopLevel(self, listener, topLevelName):
        for key in self.__IDmap:
            if (key == listener.getID()):
                raise Exception("Error, %s object is already in the input tree"%listener.__class__.__name__)
        if (isinstance(listener, InputListener)):
            temp = InputTreeNode(listener)
            self.__IDmap[listener.getID()] = temp
            DictUtil.tryFetch(self.__nodes, topLevelName, "Provided name: '%s' is not a top level node name"%topLevelName).append(temp)
            
    def setupPriority(self, listOfPriorities):
        self.__nodes = {}
        for prio in listOfPriorities:
            self.__nodes[prio] = []
        self.__priority = listOfPriorities[:]

    def update(self, deltaTime):
        for evt in pygame.event.get():
            self.__propogateEvent(evt)

    def __propogateEvent(self, evt):
        for key in self.__priority:
            for listener in self.__nodes[key]:
                if listener.sendEvent(evt):
                    return

    def lateUpdate(self):
        pass
    
    def _getNodeFromListener(self, listener):
        return self.__IDmap[listener.getID()]
    
    def bringFocus(self, listener):
        if listener.getID() in self.__IDmap:
            listenerNode = self._getNodeFromListener(listener)
            if listenerNode._parentNode != None:
                listenerNode._parentNode.bringFocus(listenerNode)
            else:
                for key in self.__nodes:
                    if listenerNode in self.__nodes[key]:
                        temp = self.__nodes[key].pop(self.__nodes[key].index(listenerNode))
                        self.__nodes[key].insert(0, temp)
                        return

        else:
            raise Exception("Error, %s object is not a listener that has been registered"%listener.__class__.__name__)
                    
class InputListener(object):
    def addListener(self, child):
        InputManager.instance()._addListener(child, self)

    def registerToManager(self, priority):
        InputManager.instance()._addToTopLevel(self, priority)
    
    def bringFocus(self):
        InputManager.instance().bringFocus(self)

    def onEvent(self, evt):
        raise Exception("Error, 'onEvent' is not implemented in '%s'."%(self.__class__.__name__))
    
    def getID(self):
        return id(self)

class InputTreeNode(object):
    def __init__(self, obj):
        self.ID = self.getID()
        self.__nodes = []
        self._parentNode = None
        self.setObj(obj)
    
    def setObj(self, listener):
        if (isinstance(listener, InputListener)):
            self.obj = listener
        else:
            raise Exception("Error, %s is not an inputListener being added to the tree"%listener.__class__.__name__)
        
    def addNode(self, node):
        if (isinstance(node,InputTreeNode)):
            self.__nodes.append(node)
            node._parentNode = self
        else:
            raise Exception("Error, %s is not an inputTreeNode being added to the tree"%node.__class__.__name__)
    
    def sendEvent(self, evt):
        if (self.obj.onEvent(evt)):
            return True
        for node in self.__nodes:
            if (node.sendEvent(evt)):
                return True
        return False
    
    def bringFocus(self, node):
        temp = self.__nodes.pop(self.__nodes.index(node))
        self.__nodes.insert(0, temp)
    
    def getID(self):
        return id(self)
        
Singleton.transformToSingleton(InputManager)
        
