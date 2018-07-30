import time
from util.bot_collections import EntityUtil, LLDict
from util.pattern.bot_eventqueue import EventQueue
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
        self.__gameObjects = LLDict()
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

            it = self.__gameObjects.begin()
            while it != self.__gameObjects.end():
                it.getValue().update(deltaTime)
                it = it.next()

            self.__impl.lateUpdate()

            it = self.__gameObjects.begin()
            while it != self.__gameObjects.end():
                it.getValue().lateUpdate()
                it = it.next()

            self.pump()

        # Sanity check for remaining objects
        objs = []
        it = self.__gameObjects.begin()
        while it != self.__gameObjects.end():
            objs.append(it.getValue().getName())
            it = it.next()
        if objs:
            raise Exception("Fatal: GameApplication still has remaining objects at time of exit\n%s" % "\n".join(objs))

        self.__impl.shutdown()

    def addObject(self, obj):
        self.__gameObjects.insert(obj.getName(), obj, "GameObject %s already exists in GameApplication" % obj.getName())
        obj._onEnter()

    def removeObject(self, obj):
        name = obj.getName()
        obj = self.__gameObjects.get(name, "Attempting to remove non-existent GameObject %s from GameApplication" % name)
        obj._onExit()
        self.__gameObjects.remove(name)

    def getGameObject(self, name):
        return self.__gameObjects.get(name, "Gameobject: %s being fetched does not exist" % name)

    def quitApp(self):
        self.__running = False

class GameObject(object):
    def __init__(self, initComponents, name=None):
        self.__name = [name, EntityUtil.genName(self)][name == None]
        self.__components = LLDict()
        self.__inApp = False # is this object already in the game stage?

        for component in initComponents:
            self.addComponent(component)
        self.pump()

    def _onEnter(self):
        self.__inApp = True
        it = self.__components.begin()
        while it != self.__components.end():
            it.getValue().onEnter()
            it = it.next()

    def _onExit(self):
        self.__inApp = False
        it = self.__components.begin()
        while it != self.__components.end():
            it.getValue().onExit()
            it = it.next()

    def addComponent(self, comp):
        self.__components.insert(comp.getName(), comp, "Component %s already exists inside of GameObject" % comp.getName())
        comp._bindToParent(self)
        if self.__inApp:
            comp.onEnter()

    def removeComponent(self, comp):
        name = comp.getName()
        comp = self.__components.get(name, "Component %s is trying to be removed from %s but does not exist" %
                                     (name, self.__class__.__name__))
        if self.__inApp:
            comp.onExit()
        comp._unbindFromParent(self)
        self.__components.remove(name)

    def getComponent(self, name):
        return self.__components.get(name, "Component %s being fetched does not exist" % name)

    def update(self, dt):
        it = self.__components.begin()
        while it != self.__components.end():
            it.getValue().onUpdate(dt)
            it = it.next()

    def lateUpdate(self):
        it = self.__components.begin()
        while it != self.__components.end():
            it.getValue().onLateUpdate()
            it = it.next()
        self.pump()

    def destroy(self):
        GameApplication.instance().removeObject(self)

    def getName(self):
        return self.__name

class GameObjectComponent(object):
    def __init__(self, name=None):
        self.__name = [name, EntityUtil.genName(self)][name == None]
        self.__parentGameObject = None

    def _bindToParent(self, parentGameObject):
        if self.__parentGameObject != None:
            raise Exception("Fatal, trying to bind %s to %s when already bound to %s" %
                            (self.getName(), parentGameObject.getName(), self.__parentGameObject.getName()))
        self.__parentGameObject = parentGameObject
        self.onBind()

    def _unbindFromParent(self, parentGameObject):
        if self.__parentGameObject == None:
            raise Exception("Fatal, trying to unbind %s from non-existent parent %s" %
                            (self.getName(), parentGameObject.getName()))
        if self.__parentGameObject != parentGameObject:
            raise Exception("Fatal, trying to unbind %s from supposed parent %s, actual parent %s" %
                            (self.getName(), parentGameObject.getName(), self.__parentGameObject.getName()))
        self.onUnbind()
        self.__parentGameObject = None

    def getParent(self):
        return self.__parentGameObject

    def getName(self):
        return self.__name

    def onUpdate(self, deltaTime):
        raise Exception("Error, %s must define 'onUpdate'" % self.__class__.__name__)

    def onLateUpdate(self):
        raise Exception("Error, %s must define 'onLateUpdate'" % self.__class__.__name__)

    def onEnter(self):
        #raise Exception("Error, %s must define 'onEnter'" % self.__class__.__name__)
        pass

    def onExit(self):
        #raise Exception("Error, %s must define 'onExit'" % self.__class__.__name__)
        pass

    def onBind(self):
        #raise Exception("Error, %s must define 'onBind'" % self.__class__.__name__)
        pass

    def onUnbind(self):
        #raise Exception("Error, %s must define 'onUnbind'" % self.__class__.__name__)
        pass

# we actually want add/removes weighted the same so that resolution is in the order of calling
def __GameObjectQueue():
    QUEUED_METHODS = [GameObject.addComponent, GameObject.removeComponent]
    EventQueue.enQueueify(GameObject, QUEUED_METHODS, lambda eventA, eventB : 0)

def __GameAppQueue():
    QUEUED_METHODS = [GameApplication.addObject, GameApplication.removeObject]
    EventQueue.enQueueify(GameApplication, QUEUED_METHODS, lambda eventA, eventB : 0)
    
__GameAppQueue()    
__GameObjectQueue()

Singleton.transformToSingleton(GameApplication)

