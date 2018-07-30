from bot_framework.bot_GOSS import GameObjectComponent, GameApplication
from bot_framework.bot_physics import BOTPhysicsSpace
from bot_framework.bot_render import BOTRenderer
from util.bot_math import Transform, Vector2
from argparse import Action

'''
This file is primarily used to provide gluing aid when integrating
the different subsystems with the GameObject Subsystem.
'''

'''
For now, all components force their renderable to be part of
a single scene, specified during creation... We might allow
the scene to changeable later...
'''
class ComponentNameUtil:
    INPUTLISTENER = "inputListener"
    RENDER = "renderable"
    RIGIDBODY = "rigidbody"
    POSITIONSYNC = "positionsync"

class RenderableComponent(GameObjectComponent):
    def __init__(self, renderable, sceneName, name=None):
        super(RenderableComponent, self).__init__(name)
        self.__renderable = renderable
        self.__sceneName = sceneName

    def getRenderable(self):
        return self.__renderable

    def onUpdate(self, dt):
        pass

    def onLateUpdate(self):
        pass

    def onEnter(self):
        renderer = BOTRenderer.instance()
        renderer.registerRenderable(self.__renderable)
        renderer.getScene(self.__sceneName).addRenderable(self.__renderable)

    def onExit(self):
        renderer = BOTRenderer.instance()
        renderer.getScene(self.__sceneName).removeRenderable(self.__renderable)
        renderer.unregisterRenderable(self.__renderable)

    def onBind(self):
        pass

    def onUnbind(self):
        pass

class RigidBodyComponent(GameObjectComponent):
    def __init__(self, rigidBodyObject, name=None):
        super(RigidBodyComponent, self).__init__(name)
        self.__rbo = rigidBodyObject

    def getRigidBodyObject(self):
        return self.__rbo

    def onUpdate(self, dt):
        pass

    def onLateUpdate(self):
        pass

    def onEnter(self):
        BOTPhysicsSpace.instance().addRigidBody(self.__rbo)

    def onExit(self):
        BOTPhysicsSpace.instance().removeRigidBody(self.__rbo)

    def onBind(self):
        pass

    def onUnbind(self):
        pass
    
    def getTransform(self):
        return self.__rbo.getTransform()

class PositionSync(GameObjectComponent):
    def __init__(self, position = Vector2()):
        self.__position = position.copy()
        self.__sync = []
        self.__source = None
        super(PositionSync, self).__init__(ComponentNameUtil.POSITIONSYNC)

    def onUpdate(self, dt):
        pass
    
    def onLateUpdate(self):
        if self.__source != None:
            self.__source.position.copyTo(self.__position)
            for trans in self.__sync:
                self.__source.position.copyTo(trans.position)
        else:
            for trans in self.__sync:
                self.__position.copyTo(trans.position)
        
    def syncTransform(self, transform):
        self.__sync.append(transform)

    def syncFrom(self, transform):
        self.__source = transform
        self.__position = transform.position.copy()
        
    def getPosition(self):
        return self.position
    
class ProjectileEmitter(GameObjectComponent):
    def __init__(self, renderable, behaviour):
        super(ProjectileEmitter, self).__init__([renderable, behaviour], "projectile")

'''
This class should return a position as a function of time
this position should be the path that the projectile takes in flight
Positive Y is the forward direction
'''
class ProjectilePath(object):
    def getPos(self, dt):
        raise Exception("Error, %s must define 'getPos'" % self.__class__.__name__)
