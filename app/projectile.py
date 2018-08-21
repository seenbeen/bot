import math
import pygame

from util.bot_collections import DictUtil
from util.bot_integration import RenderableComponent, RigidBodyComponent, ComponentNameUtil, ColliderTagsUtil, PositionSync, ProjectilePath, ProjectileEmitter
from util.bot_math import Vector2
from util.bot_logger import Logger

from bot_framework.bot_assetManager import AssetManager
from bot_framework.bot_GOSS import GameObject, GameObjectComponent, GameApplication
from bot_framework.bot_physics import BOTPhysicsRigidBody, BOTPhysicsCollider, BOTPhysicsCollisionResolver
from bot_framework.bot_render import BOTSprite

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
        def __init__(self, pather, dmg, name = ComponentNameUtil.MAINSCRIPT):
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
            
        def getDamage(self):
            return self.dmg
        
            
    def __init__(self, pos, dmg, pather, sceneName, sprite, name=None):
        
        rcomp = RenderableComponent(sprite, sceneName, ComponentNameUtil.RENDER)
        
        script = Projectile.Script(pather, dmg)
        
        rbocomp = RigidBodyComponent(BOTPhysicsRigidBody(script,
                                                         BOTPhysicsCollider(sprite._genBounds()),
                                                         ColliderTagsUtil.PROJECTILE),
                                     ComponentNameUtil.RIGIDBODY)
        
        syncer = PositionSync(pos)
        syncer.syncTransform(sprite.transform)
        syncer.syncTransform(rbocomp.getTransform())
        
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
        
class EnemyProjectileResolver(BOTPhysicsCollisionResolver):
        def __init__(self):
            super(EnemyProjectileResolver,
                  self).__init__(ColliderTagsUtil.ENEMY, ColliderTagsUtil.PROJECTILE)

        def onResolve(self, enemy, projectile):
            enemyScript = enemy.getBoundObj()
            proj = projectile.getBoundObj()
            enemyScript.dealDamage(proj.getDamage())
            
            GameApplication.instance().removeObject(proj.getParent())
            # pretend during this update fireball obj also went peace due to collision
            #physx.removeRigidBody(rbFireball)
            
