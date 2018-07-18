import pygame
from util.bot_math import Vector2
from util.pattern.bot_singleton import Singleton
from util.bot_collections import DictUtil

class InputManager(object):
    def __init__(self):
        self.__nodes = {}
        self.__priority = []
        self.__IDmap = {}

    '''
    Listeners can be passed in by reference
    Parents can be passed in by reference or by ID
    In both cases, the InputManager will set Listener to be a child of Parent
    '''
    def _addListener(self, listener, parent):
        if listener.getName() in self.__IDmap:
            raise Exception("Error, %s object is already in the input tree"%listener.__class__.__name__)
        if (isinstance(listener, InputListener)):
            temp = InputTreeNode(listener)
            self.__IDmap[listener.getName()] = temp
            
            if isinstance(parent, str):
                DictUtil.tryFetch(self.__IDmap, parent.getName(), "Provided object: '%s' has not been added to the input tree"%parent.__class__.__name__)._addNode(temp)
                temp._parentNode = self.__IDmap[parent]
            elif (isinstance(parent, InputListener)):
                DictUtil.tryFetch(self.__IDmap, parent.getName(), "Provided object: '%s' has not been added to the input tree"%parent.__class__.__name__)._addNode(temp)
                temp._parentNode = self._getNodeFromListener(parent)
            else:
                raise Exception("provided object: '%s' is not a correct type to be a parent to an Input Node"%parent.__class__.__name__)
                
        else:
            raise Exception("provided object: '%s' is not an input listener"%listener.__class__.__name__)
    
    
    '''
    When adding a listener to the TOP level of nodes, this function is used instead.
    priorityKey is a key name that was defined in setupPriority
    '''
    def _addToTopLevel(self, listener, priorityKey):
        for key in self.__IDmap:
            if (key == listener.getName()):
                raise Exception("Error, %s object is already in the input tree"%listener.__class__.__name__)
        if (isinstance(listener, InputListener)):
            temp = InputTreeNode(listener)
            self.__IDmap[listener.getName()] = temp
            DictUtil.tryFetch(self.__nodes, priorityKey, "Provided name: '%s' is not an existing top level key"%priorityKey).append(temp)
            
    '''
    When using the inputmanager, you must setup a top level priority list.
    This list will allow you to add new listeners to the top level easily.
    Example: [UI", "Menu", "GameObjects"]
    
    The input manager will not work without this being setup first
    '''
    def setupPriority(self, listOfPriorities):
        self.__nodes = {}
        for prio in listOfPriorities:
            self.__nodes[prio] = []
        self.__priority = listOfPriorities[:]

    '''
    passes all events down
    '''
    def update(self, deltaTime):
        for evt in pygame.event.get():
            self.__propogateEvent(evt)

    '''
    Passes events through each list based on the order defined during setupPriority
    '''
    def __propogateEvent(self, evt):
        for key in self.__priority:
            for listener in self.__nodes[key]:
                if listener._sendEvent(evt):
                    return
    
    def lateUpdate(self):
        pass
    '''
    returns the associated node, given a listener
    '''
    def _getNodeFromListener(self, listener):
        return DictUtil.tryFetch(self.__IDmap, listener.getName(), "listener: %s has not been added to the input manager"%listener.__class__.__name__)
    
    '''
    This function will bring a listener to the head of it's parents list.
    being at the head of a list will ensure that events are passed to it first, before other listeners belonging to the same parent.
    '''
    def _bringFocus(self, listener):
        if listener.getName() in self.__IDmap:
            listenerNode = self._getNodeFromListener(listener)
            if listenerNode._parentNode != None:
                listenerNode._parentNode._bringFocus(listenerNode)
            else:
                for key in self.__nodes:
                    if listenerNode in self.__nodes[key]:
                        temp = self.__nodes[key].pop(self.__nodes[key].index(listenerNode))
                        self.__nodes[key].insert(0, temp)
                        return

        else:
            raise Exception("Error, %s object is not a listener that has been registered"%listener.__class__.__name__)
                    
class InputListener(object):
    '''
    Adds another listener as a child of this object
    child must be a listener reference
    '''
    def addListener(self, child):
        InputManager.instance()._addListener(child, self)
    '''
    Registers listener to the given priority key of the manager
    '''
    def registerToManager(self, priority):
        InputManager.instance()._addToTopLevel(self, priority)
    
    '''
    Calling this function will bring the listener to the head of the parent it belongs to
    This will ensure that any event that is passed down from the parent will be sent to this first
    '''
    def bringFocus(self):
        InputManager.instance()._bringFocus(self)

    def onEvent(self, evt):
        raise Exception("Error, 'onEvent' is not implemented in '%s'."%(self.__class__.__name__))
    
    def getName(self):
        return str(id(self))+self.__class__.__name__

class InputTreeNode(object):
    def __init__(self, listener):
        self.__nodes = []
        self._parentNode = None
        self.listener = listener
    
    '''
    Adds another node as child of this node
    '''
    def _addNode(self, node):
        if (isinstance(node,InputTreeNode)):
            self.__nodes.append(node)
            node._parentNode = self
        else:
            raise Exception("Error, %s is not an inputTreeNode"%node.__class__.__name__)
    '''
    Calls own onEvent, then propogates event to children if not blocked
    '''
    def _sendEvent(self, evt):
        if (self.listener.onEvent(evt)):
            return True
        for node in self.__nodes:
            if (node._sendEvent(evt)):
                return True
        return False
    
    def _bringFocus(self, node):
        temp = self.__nodes.pop(self.__nodes.index(node))
        self.__nodes.insert(0, temp)
    
    def getName(self):
        return str(id(self))+self.__class__.__name__
        
Singleton.transformToSingleton(InputManager)

