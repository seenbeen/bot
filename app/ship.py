from util.bot_collections import DictUtil
from util.bot_integration import RenderableComponent
from bot_framework.bot_assetManager import AssetManager
from bot_framework.bot_GOSS import GameObject, GameObjectComponent
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

        def onUpdate(self, dt):
            r = self.shipSprite.transform.rotation
            self.shipSprite.transform.rotation = (r + dt * 30) % 360

        def onLateUpdate(self):
            pass

        def onEnter(self):
            print "%s onEnter" % self.getName()

        def onExit(self):
            print "%s onExit" % self.getName()

        def onBind(self):
            print "%s onBind" % self.getName()
            self.shipSprite = self.getParent().getComponent("SpriteComp").getRenderable()

        def onUnbind(self):
            print "%s onUnbind" % self.getName()
            self.shipSprite = None

    def __init__(self, sceneName, name=None):
        rcomp = RenderableComponent(Ship.__Sprite("banking_left"), sceneName, "SpriteComp")
        script = Ship.__Script()
        comps = [rcomp, script]
        super(Ship, self).__init__(comps, name)
