from bot_framework.bot_GOSS import GameObjectComponent, GameApplication
from bot_framework.bot_physics import BOTPhysicsSpace
from bot_framework.bot_render import BOTRenderer

'''
This file is primarily used to provide gluing aid when integrating
the different subsystems with the GameObject Subsystem.
'''

'''
For now, all components force their renderable to be part of
a single scene, specified during creation... We might allow
the scene to changeable later...
'''
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
