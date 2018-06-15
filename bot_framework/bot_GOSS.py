import time
from bot_framework.bot_fsm import *
from util.pattern.bot_singleton import Singleton

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
                
        self.__impl.shutdown()
        
    def addObject(self, obj):
        if (obj.name in self.__gameObjects):
            raise Exception('Error, %s gameobject has been added to a game object multiple times'%obj.name)
        self.__gameObjects[obj.name] = obj
    
    def removeObject(self, name):
        if (name in self.__gameObjects):
            del self.__gameObjects[name]
        else:
            raise Exception('Error, Attempting to delete non-existent component:%s from game object'%name)
    
    def getGameObjects(self):
        return self.__gameObjects
    
    def getGameObject(self, name):
        return self.__gameObjects[name]
    
    def quit(self):
        self.__running = False
        
class GameObject(object):
    def __init__(self, listofComponents, name):
        self.name = name
        self.__components = {}
        for comp in listofComponents:
            self.addComponent(comp)
        
    def addComponent(self, comp):
        if (comp.name in self.__components):
            raise Exception('Error, %s component has been added to a game object multiple times'%comp.name)
        self.__components[comp.name] = comp
        if (isinstance(comp, ScriptComponent)):
            comp._setParent(self)
        
    def removeComponent(self, name):
        if (name in self.__components):
            del self.__components[name]
        else:
            raise Exception('Error, Attempting to delete non-existent component:%s from game object'%name)
    
    def update(self, dt):
        for comp in self.__components:
            self.__components[comp].update(dt)
            
    def lateUpdate(self):
        for comp in self.__components:
            self.__components[comp].lateUpdate()
            
    def destroy(self):
        for comp in self.__components:
            self.removeComponent(comp.name)
        self.__del__()
          
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

    def update(self, deltaTime):
        raise Exception('Error, %s must define a update method'%self.__class__.__name__)

    def lateUpdate(self):
        raise Exception('Error, %s must define a late update method'%self.__class__.__name__)

Singleton.transformToSingleton(GameApplication)
