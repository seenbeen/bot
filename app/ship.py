import math

from util.bot_collections import DictUtil
from util.bot_integration import RenderableComponent, RigidBodyComponent
from util.bot_math import Vector2

from bot_framework.bot_assetManager import AssetManager
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
        def __init__(self, name=None):
            super(self.__class__, self).__init__(name)
            self.shipSprite = None
            self.rbo = None

        def onUpdate(self, dt):
            r = self.shipSprite.transform.rotation
            newR = (r + dt * 60) % 360
            self.shipSprite.transform.rotation = newR
            v = Vector2(math.cos(math.radians(newR + 90)),
                        math.sin(math.radians(newR + 90))) * 50
            v.copyTo(self.rbo.getVelocity())

        def onLateUpdate(self):
            self.rbo.getTransform().position.copyTo(self.shipSprite.transform.position)

        def onEnter(self):
            print "%s onEnter" % self.getName()

        def onExit(self):
            print "%s onExit" % self.getName()

        def onBind(self):
            print "%s onBind" % self.getName()
            self.shipSprite = self.getParent().getComponent("SpriteComp").getRenderable()
            self.rbo = self.getParent().getComponent("RBComp").getRigidBodyObject()

        def onUnbind(self):
            print "%s onUnbind" % self.getName()
            self.shipSprite = None
            self.rbo = None

    def __init__(self, sceneName, name=None):
        sprite = Ship.__Sprite("banking_left")
        sprite.transform.scale *= Vector2(-1, 1) # bank right
        rcomp = RenderableComponent(sprite, sceneName, "SpriteComp")
        script = Ship.__Script()
        rbocomp = RigidBodyComponent(BOTPhysicsRigidBody(script,
                                                         BOTPhysicsCollider(sprite._genBounds()),
                                                         "SHIP_TAG"),
                                     "RBComp")
        comps = [rcomp, rbocomp, script]
        super(Ship, self).__init__(comps, name)
