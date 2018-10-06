import math
import pygame

from projectile import BasicPlaneProj

from util.bot_collections import DictUtil
from util.bot_integration import RenderableComponent, RigidBodyComponent, ComponentNameUtil, PositionSync, ProjectileEmitter
from util.bot_math import Vector2
from util.bot_logger import Logger

from bot_framework.bot_assetManager import AssetManager
from bot_framework.bot_inputmanager import InputManager, InputListener
from bot_framework.bot_GOSS import GameObject, GameObjectComponent
from bot_framework.bot_physics import BOTPhysicsRigidBody, BOTPhysicsCollider
from bot_framework.bot_render import BOTSprite

class Ship(GameObject):
    class __Sprite(BOTSprite):
        def __init__(self, initAnimKey="still"):
            animSet = AssetManager.instance().loadAsset("assets/raiden.bsprite")
            startKey = initAnimKey
            startFrames = DictUtil.tryFetch(animSet, startKey)

            super(self.__class__, self).__init__(startKey, startFrames)
            for animKey in animSet:
                if animKey != startKey:
                    self.addAnimation(animKey, animSet[animKey])

            self.debug = True

    class __Script(GameObjectComponent):
        def __init__(self, name = ComponentNameUtil.MAINSCRIPT ):
            super(self.__class__, self).__init__(name)
            self.shipSprite = None
            self.rbo = None
            self.listener = None
            self.emitter = None
            self.coolDown = 0.0

        def onUpdate(self, dt):
            '''
            r = self.shipSprite.transform.rotation
            newR = (r + dt * 60) % 360
            self.shipSprite.transform.rotation = newR
            v = Vector2(math.cos(math.radians(newR + 90)),
                        math.sin(math.radians(newR + 90))) * 50
            v.copyTo(self.rbo.getVelocity())
            '''
            vel = self.rbo.getVelocity()
            if (self.listener.getCondition('up')):
                vel += Vector2(0, 1)
                
            if (self.listener.getCondition('down')):
                vel += Vector2(0, -1)
                
            if (self.listener.getCondition('left')):
                vel += Vector2(-1, 0)
                
            if (self.listener.getCondition('right')):
                vel += Vector2(1, 0)
            vel *= 0.99
            
            vel.copyTo(self.rbo.getVelocity())
            
            if (self.listener.getCondition('action')):
                if (self.coolDown < 0.0):
                    self.emitter.spawnProjectile()
                    self.coolDown = 1.0
                
            self.coolDown -= dt
                
            #Logger.instance().log(str(self.rbo.getVelocity()))

        def onLateUpdate(self):
            #self.rbo.getTransform().position.copyTo(self.shipSprite.transform.position)
            pass

        def onEnter(self):
            print "%s onEnter" % self.getName()

        def onExit(self):
            print "%s onExit" % self.getName()

        def onBind(self):
            print "%s onBind" % self.getName()
            self.shipSprite = self.getParent().getComponent(ComponentNameUtil.RENDER).getRenderable()
            self.rbo = self.getParent().getComponent(ComponentNameUtil.RIGIDBODY).getRigidBodyObject()
            self.listener = self.getParent().getComponent(ComponentNameUtil.INPUTLISTENER)
            self.emitter = self.getParent().getComponent("ProjectileEmitter")

        def onUnbind(self):
            print "%s onUnbind" % self.getName()
            self.shipSprite = None
            self.rbo = None

    def __init__(self, sceneName, name=None):
        sprite = Ship.__Sprite("banking_left")
        sprite.transform.scale *= Vector2(-1, 1) # bank right
        rcomp = RenderableComponent(sprite, sceneName, ComponentNameUtil.RENDER)
        script = Ship.__Script("ShipScript")
        rbocomp = RigidBodyComponent(BOTPhysicsRigidBody(script,
                                                         BOTPhysicsCollider(sprite._genBounds()),
                                                         "SHIP_TAG"),
                                     ComponentNameUtil.RIGIDBODY)
        
        emitter = ProjectileEmitter(BasicPlaneProj, sceneName, Vector2(0,10))
        
        syncer = PositionSync()
        syncer.syncFrom(rbocomp.getTransform())
        syncer.syncTransform(sprite.transform)
        
        
        listen = ShipListener(ShipListener.DEFAULT)
        comps = [rcomp, rbocomp, listen, syncer, emitter, script]
        super(Ship, self).__init__(comps, name)
        
class ShipListener(GameObjectComponent, InputListener):
    DEFAULT = {'action':pygame.K_z, 'left':pygame.K_LEFT, 'right':pygame.K_RIGHT, 'up':pygame.K_UP, 'down':pygame.K_DOWN}
    
    def __init__(self, keyConfig):
        self.__keyConfig = keyConfig
        self.__inputs = {}
        self.__inputPool = []
        for key in self.__keyConfig:
            self.__inputs[key] = False
            self.__inputPool.append(self.__keyConfig[key])
        self.registerToManager("GAME")
        super(ShipListener, self).__init__(ComponentNameUtil.INPUTLISTENER)
        
    def onEvent(self, evt):
        if evt.type == pygame.KEYDOWN and evt.key in self.__inputPool:
            for key in self.__keyConfig:
                if evt.key == self.__keyConfig[key]:
                    self.__inputs[key] = True
                    return True
        elif evt.type == pygame.KEYUP and evt.key in self.__inputPool:
            for key in self.__keyConfig:
                if evt.key == self.__keyConfig[key]:
                    self.__inputs[key] = False
                    return True
        return False
    
    def onUpdate(self, dt):
        pass
    
    def onLateUpdate(self):
        pass
    
    def getCondition(self, key):
        return DictUtil.tryFetch(self.__inputs, key, "Error, %s is not a valid input condition for this input listener"%key)
    
    def onBind(self):
        pass
