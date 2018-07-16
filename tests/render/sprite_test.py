import os
import time
import math
import pygame

from util.bot_asset_util import AssetUtil
from util.bot_collections import DictUtil
from util.bot_math import *

from bot_framework.bot_assetManager import AssetManager
from bot_framework.bot_render import *


# this test involves a bit more integration, as
# it uses both stuff from renderer and asset manager
def run():
    def rotatePt(r, ang):
        a = math.radians(ang)
        return Vector2(r * math.cos(a), r * math.sin(a))

    def genTri(longRad, shortRad):
        return [Vector2(0, shortRad), Vector2(longRad, 0), Vector2(0, 0)]

    class ToruSprite(BOTSprite):
        def __init__(self, initAnimKey="swingOF"):
            animSet = AssetManager.instance().loadAsset("assets/toru.bsprite")
            startKey = initAnimKey
            startFrames = DictUtil.tryFetch(animSet, startKey)

            super(ToruSprite, self).__init__(startKey, startFrames)
            for animKey in animSet:
                if animKey != startKey:
                    self.addAnimation(animKey, animSet[animKey])

    # init AssetManager
    listFile = "tests/render/assetsList"
    pathLocation = "tests/render/"

    print "Running AssetLister..."
    os.system("python scripts/bot_assetLister.py " + listFile + " " + pathLocation)
    
    AssetManager.initialize(pathLocation)
    assetManager = AssetManager.instance()
    assetManager.loadTypeCallback(".bsprite", AssetUtil.loadSpriteSheet)

    print "Loading Assets..."
    AssetManager.instance().load(listFile)
    
    # init renderer
    BOTRenderer.initialize(800, 600)
    renderer = BOTRenderer.instance()

    # configure renderer

    # create Scenes
    gameScene = BOTScene()
    renderer.registerScene(gameScene)

    uiScene = BOTScene()
    renderer.registerScene(uiScene)

    # create cameras
    gameCameraP1 = BOTCamera(400, 600)
    gameCameraP2 = BOTCamera(400, 600)

    gameCameraP2.transform.scale *= 1.25

    renderer.registerCamera(gameCameraP1)
    renderer.registerCamera(gameCameraP2)

    # ui camera
    uiCamera = BOTCamera(800, 600)
    uiCamera.transform.position += Vector2(400, 300)
    renderer.registerCamera(uiCamera)

    # create viewports
    gameViewportP1 = BOTViewport(400, 600)
    gameViewportP2 = BOTViewport(400, 600)
    gameViewportP2.position += Vector2(400, 0)

    renderer.registerViewport(gameViewportP1)
    renderer.registerViewport(gameViewportP2)

    # ui viewport
    uiViewport = BOTViewport(800, 600)
    renderer.registerViewport(uiViewport)

    # create Compositing Chain
    camCompositorP1 = BOTCameraCompositor(gameScene.getName(), gameCameraP1.getName(),
                                          gameViewportP1.getName(),
                                          BOTCompositingCache.getScreenKey())
    camCompositorP2 = BOTCameraCompositor(gameScene.getName(), gameCameraP2.getName(),
                                          gameViewportP2.getName(),
                                          BOTCompositingCache.getScreenKey())
    
    renderer.chainCompositor(camCompositorP1)
    renderer.chainCompositor(camCompositorP2)

    # ui compositor comes last (shows up first)
    uiCompositor = BOTCameraCompositor(uiScene.getName(), uiCamera.getName(),
                                       uiViewport.getName(),
                                       BOTCompositingCache.getScreenKey())

    renderer.chainCompositor(uiCompositor)

    # create renderables
    player1 = ToruSprite()
    player1.transform.scale *= Vector2(-1, 1)
    player2 = ToruSprite("walk1")
    player2.transform.position += gameCameraP2.transform.position

    renderer.registerRenderable(player1) # important! otherwise will not animate
    renderer.registerRenderable(player2)
    gameScene.addRenderable(player1)
    gameScene.addRenderable(player2)

    # to make things easier to track, let's add some camera position trackers
    cam1Poly = BOTPolygon(genTri(20, 10), (255, 0, 0))
    cam2Poly = BOTPolygon(genTri(20, 10), (0, 0, 255))

    gameScene.addRenderable(cam1Poly)
    gameScene.addRenderable(cam2Poly)

    # again, not sure if direct assignment should be advised...
    cam1Poly.transform = gameCameraP1.transform
    cam2Poly.transform = gameCameraP2.transform

    # ui stuff gets added to ui scene - for now just a bar to divide the 2 screens
    uiDividerPoly = BOTPolygon(map(lambda x: Vector2(*x),[[0, 0],[0, 600],[0, 0]]), (0, 0, 0))
    uiDividerPoly.transform.position = Vector2(400, 0)

    uiScene.addRenderable(uiDividerPoly)

    # game loop stuff, should be integrated with GOSS soon
    running = True

    start = time.time()

    p2Rotation = 0
    while running:
        currentTime = time.time()
        deltaTime = currentTime - start
        start = currentTime
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False;

        p2Rotation = (p2Rotation + deltaTime * 60) % 360
        gameCameraP2.transform.position = rotatePt(175, -p2Rotation)
        player2.transform.position = Vector2() + gameCameraP2.transform.position # no copy yet so simulate one...
        player2.transform.scale.x = [1, -1][p2Rotation > 180]
        renderer.update(deltaTime)

    renderer.shutdown()
