import math
import pygame

from util.bot_collections import DictUtil
from util.bot_integration import RenderableComponent, RigidBodyComponent, ComponentNameUtil, ColliderTagsUtil, PositionSync, ProjectilePath, ProjectileEmitter
from util.bot_math import Vector2
from util.bot_logger import Logger

from bot_framework.bot_assetManager import AssetManager
from bot_framework.bot_GOSS import GameObject, GameObjectComponent, GameApplication
from bot_framework.bot_physics import BOTPhysicsRigidBody, BOTPhysicsCollider
from bot_framework.bot_render import BOTSprite


class Enemy(GameObject):
    class Script(GameObjectComponent):
        def __init__(self, hp, name = ComponentNameUtil.MAINSCRIPT):
            super(self.__class__, self).__init__(name)
            self.rbo = None
            self.render = None
            self.sync = None
            self.hp = hp
            
        def onUpdate(self, dt):
            pass
        
        def onLateUpdate(self):
            pass
            
        def onBind(self):
            self.render = self.getParent().getComponent(ComponentNameUtil.RENDER).getRenderable()
            self.rbo = self.getParent().getComponent(ComponentNameUtil.RIGIDBODY).getRigidBodyObject()
            self.sync = self.getParent().getComponent(ComponentNameUtil.POSITIONSYNC)
            
        def dealDamage(self, dmg):
            self.hp -= dmg
            if (self.hp <= 0):
                GameApplication.instance().removeObject(self.getParent())
            
    def __init__(self, pos, hp, sceneName, sprite, name=None):
        
        rcomp = RenderableComponent(sprite, sceneName, ComponentNameUtil.RENDER)
        
        script = Enemy.Script(hp)
        
        rbocomp = RigidBodyComponent(BOTPhysicsRigidBody(script,
                                                         BOTPhysicsCollider(sprite._genBounds()),
                                                         ColliderTagsUtil.ENEMY),
                                     ComponentNameUtil.RIGIDBODY)
        
        syncer = PositionSync()
        syncer.syncFrom(rbocomp.getTransform())
        syncer.syncTransform(sprite.transform)
        
        comps = [rcomp, syncer, rbocomp, script]
        super(Enemy, self).__init__(comps, name)
        
class BasicPlaneEnemy(Enemy):
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
        asset = AssetManager.instance().loadAsset("assets/raiden.bsprite")
        sprite = BasicPlaneEnemy.__Sprite(asset, "still")
        super(BasicPlaneEnemy, self).__init__(pos, 5, sceneName, sprite)