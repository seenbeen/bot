import time
from bot_framework.bot_fsm import *
from util.pattern.bot_singleton import Singleton
from util.pattern.bot_eventqueue import *
from util.bot_collections import DictUtil

class GameAppImpl:
    def initialize(self):
        raise Exception('Error, %s must define initializeSubsystems'%self.__class__.__name__)
    
    def shutdown(self):
        raise Exception('Error, %s must define shutdownSubsystems'%self.__class__.__name__)
    
    def update(self, deltaTime):
        raise Exception('Error, %s must define gameLoop'%self.__class__.__name__)
    
    def lateUpdate(self, deltaTime):
        raise Exception('Error, %s must define gameLoop'%self.__class__.__name__)

class GameApplication:
    def __init__(self, implementation):
        self.__gameObjects = {}
        self.__running = True
        self.__impl = implementation()
        
    def run(self):
        self.__impl.initialize()
        start = time.time()
        
        while self.__running:
            currentTime = time.time()
            deltaTime = currentTime - start
            start = currentTime
            
            self.__impl.update(deltaTime)
            
            for gObj in self.__gameObjects:
                self.__gameObjects[gObj].update(deltaTime)
                
            self.__impl.lateUpdate()
            
            for gObj in self.__gameObjects:
                self.__gameObjects[gObj].lateUpdate()
            
            self.pump()
        self.__impl.shutdown()
        
    def addObject(self, obj):
        DictUtil.tryStrictInsert(self.__gameObjects, obj.name, obj, "GameObject: %s already exists inside of GameApplication"%obj.name)
    
    def removeObject(self, name):
        DictUtil.tryRemove(self.__gameObjects, name, "GameObject: %s is trying to be removed from GameApplication but does not exist"%name)
    
    def getGameObject(self, name):
        return DictUtil.tryFetch(self.__gameObjects, name, "Gameobject: %s being fetched does not exist"%name)
    
    def quit(self):
        self.__running = False
        
class GameObject(object):
    def __init__(self, listofComponents, name):
        self.name = name
        self.__components = {}
        for comp in listofComponents:
            self.addComponent(comp)
        
    def addComponent(self, comp):
        DictUtil.tryStrictInsert(self.__components, comp.name, comp, "Component: %s already exists inside of GameObject"%comp.name)
        if (isinstance(comp, ScriptComponent)):
            comp._setParent(self)
        
    def removeComponent(self, name):
        DictUtil.tryRemove(self.__components, name, "Component: %s is trying to be removed from %s but does not exist"%name,__class__.name)
    
    def getComponent(self, name):
        return DictUtil.tryFetch(self.__components, name, "Component: %s being fetched does not exist"%name) 
    
    def update(self, dt):
        for comp in self.__components:
            self.__components[comp].update(dt)
            
    def lateUpdate(self):
        for comp in self.__components:
            self.__components[comp].lateUpdate()
        self.pump()
            
    def destroy(self):
        GameApplication.instance().removeObject(self.name)
          
class Component(object):
    def __init__(self, name):
        self.name = name

    def update(self, deltaTime):
        raise Exception('Error, %s must define a update method'%self.__class__.__name__)

    def lateUpdate(self):
        raise Exception('Error, %s must define a late update method'%self.__class__.__name__)

class ScriptComponent(object):
    def __init__(self, name):
        self.name = name
        self.gameObjectParent = None
        
    def _setParent(self, gameObjectParent):
        self.gameObjectParent = gameObjectParent
        self.onBind()
        
    def onBind(self):
        pass

    def update(self, deltaTime):
        raise Exception('Error, %s must define a update method'%self.__class__.__name__)

    def lateUpdate(self):
        raise Exception('Error, %s must define a late update method'%self.__class__.__name__)

def __GameObjectQueue():
    QUEUED_METHODS = [GameObject.addComponent, GameObject.removeComponent, GameObject.destroy]

    ADD_METH = GameObject.addComponent.__name__
    REMOVE_METH = GameObject.removeComponent.__name__
    DESTROY_METH = GameObject.destroy.__name__

    KIND_ORDER = {}
    METHOD_ORDER = {ADD_METH : 0, REMOVE_METH: 1, DESTROY_METH : 2}
    
    def pumpCompare(eventA, eventB):
        
        if eventA.name != eventB.name:
            return (METHOD_ORDER[eventA.name] - METHOD_ORDER[eventB.name])

        if eventA.name == ADD_METH:
            return 0
        elif eventA.name == REMOVE_METH:
            return 1
        elif eventA.name == DESTROY_METH:
            return 2
        else:
            raise Exception("Unexpected method %s being pumped!"%eventA.name)

    EventQueue.enQueueify(GameObject, QUEUED_METHODS, pumpCompare)

def __GameAppQueue():
    QUEUED_METHODS = [GameApplication.addObject, GameApplication.removeObject]

    ADD_METH = GameApplication.addObject.__name__
    REMOVE_METH = GameApplication.removeObject.__name__

    KIND_ORDER = {}
    METHOD_ORDER = {ADD_METH : 0, REMOVE_METH: 1}
    
    def pumpCompare(eventA, eventB):
        
        if eventA.name != eventB.name:
            return (METHOD_ORDER[eventA.name] - METHOD_ORDER[eventB.name])

        if eventA.name == ADD_METH:
            return 0
        elif eventA.name == REMOVE_METH:
            return 1
        else:
            raise Exception("Unexpected method %s being pumped!"%eventA.name)

    EventQueue.enQueueify(GameApplication, QUEUED_METHODS, pumpCompare)
    
__GameAppQueue()    
__GameObjectQueue()

Singleton.transformToSingleton(GameApplication)
