import math
import pygame

from util.bot_collections import DictUtil
from util.bot_integration import RenderableComponent, RigidBodyComponent, ComponentNameUtil, PositionSync, ProjectilePath, ProjectileEmitter
from util.bot_math import Vector2
from util.bot_logger import Logger

from bot_framework.bot_assetManager import AssetManager
from bot_framework.bot_GOSS import GameObject, GameObjectComponent
from bot_framework.bot_physics import BOTPhysicsRigidBody, BOTPhysicsCollider
from bot_framework.bot_render import BOTSprite

class basicEmitter(GameObjectComponent):
    def __init__(self):
        super(basicEmitter, self).__init__(self, "ProjectileEmmiter")
        
    def fireProjectile(self):
        temp = Projectile()
        
    
    def onUpdate(self, dt):
        pass
    def onLateUpdate(self):
        pass

class StraightPath(ProjectilePath):
    def __init__(self, speed, initPos):
        self.time = 0
        self.speed = speed
        self.__initPos = initPos
        
    def getPos(self, dt):
        self.time += dt
        return Vector2(0,self.time*self.speed) + self.__initPos

class Projectile(GameObject):
    class Script(GameObjectComponent):
        def __init__(self, pather, dmg, name="ProjectileScript"):
            super(self.__class__, self).__init__(name)
            self.pather = pather
            self.rbo = None
            self.render = None
            self.sync = None
            self.dmg = dmg
            
            
        
        def onUpdate(self, dt):
            self.pather.getPos(dt).copyTo(self.sync.getPosition())
        
        def onLateUpdate(self):
            pass
            
        def onBind(self):
            self.render = self.getParent().getComponent(ComponentNameUtil.RENDER).getRenderable()
            self.rbo = self.getParent().getComponent(ComponentNameUtil.RIGIDBODY).getRigidBodyObject()
            self.sync = self.getParent().getComponent(ComponentNameUtil.POSITIONSYNC)
            
    def __init__(self, pos, dmg, pather, sceneName, sprite, name=None):
        
        
        
        rcomp = RenderableComponent(sprite, sceneName, ComponentNameUtil.RENDER)
        
        script = Projectile.Script(pather, dmg)
        
        rbocomp = RigidBodyComponent(BOTPhysicsRigidBody(script,
                                                         BOTPhysicsCollider(sprite._genBounds()),
                                                         "PROJ_TAG"),
                                     ComponentNameUtil.RIGIDBODY)
        syncer = PositionSync()
        syncer.syncTransform(sprite.transform)
        
        
        
        comps = [rcomp, rbocomp, syncer, script]
        super(Projectile, self).__init__(comps, name)
        
class BasicPlaneProj(Projectile):
    class __Sprite(BOTSprite):
        def __init__(self, animSet, initAnimKey):
            
            startKey = initAnimKey
            startFrames = DictUtil.tryFetch(animSet, startKey)

            super(self.__class__, self).__init__(startKey, startFrames)
            for animKey in animSet:
                if animKey != startKey:
                    self.addAnimation(animKey, animSet[animKey])

            self.debug = True
    
    def __init__(self, pos, sceneName):
        pather = StraightPath(30, pos)
        asset = AssetManager.instance().loadAsset("assets/raiden.bsprite")
        sprite = BasicPlaneProj.__Sprite(asset, "still")
        super(BasicPlaneProj, self).__init__(pos, 1, pather, sceneName, sprite)