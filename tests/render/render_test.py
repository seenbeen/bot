import pygame
import math
from bot_framework.bot_render import *
from util.bot_math import *

def run():
    def rotatePt(r, ang):
        a = math.radians(ang)
        return Vector2(r * math.cos(a), r * math.sin(a))
    
    def genStar(sides, longRad, shortRad):
        return [rotatePt([shortRad, longRad][i%2], i*360/sides) for i in range(sides)]

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

    gameCameraP2.transform.position += Vector2(150, 150)
    
    renderer.registerCamera(gameCameraP1)
    renderer.registerCamera(gameCameraP2)

    # ui camera
    uiCamera = BOTCamera(800, 600)
    uiCamera.transform.position += Vector2(400, 300)
    renderer.registerCamera(uiCamera)

    # create viewports
    gameViewportP1 = BOTViewport(400, 600)
    gameViewportP2 = BOTViewport(400, 600)

    renderer.registerViewport(gameViewportP1)
    renderer.registerViewport(gameViewportP2)
    
    # mutation after registration is fine
    gameViewportP2.position += Vector2(400, 0)

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
    star = BOTPolygon(genStar(8, 100, 100 / 3.0), (0, 255, 0))
    star.debug = True # let's check out those bounding rects

    gameScene.addRenderable(star)

    # to make things easier to track, let's add some camera position trackers
    cam1Poly = BOTPolygon(genStar(4, 20, 20), (255, 0, 0))
    cam2Poly = BOTPolygon(genStar(4, 20, 20), (0, 0, 255))

    gameScene.addRenderable(cam1Poly)
    gameScene.addRenderable(cam2Poly)

    # we might actually want to prevent assignment by reference as
    # this could introduce some sketchy and hard-to-debug issues
    cam1Poly.transform = gameCameraP1.transform
    cam2Poly.transform = gameCameraP2.transform

    # ui stuff gets added to ui scene - for now just a bar to divide the 2 screens
    uiDividerPoly = BOTPolygon(map(lambda x: Vector2(*x),[[0, 0],[0, 600],[0, 0]]), (0, 0, 0))
    uiDividerPoly.transform.position = Vector2(400, 0)

    uiScene.addRenderable(uiDividerPoly)

    # game loop stuff, should be integrated with GOSS soon
    running = True

    myClock = pygame.time.Clock()
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False;

        star.transform.rotation = (star.transform.rotation + 2) % 360
        gameCameraP2.transform.rotation = (gameCameraP2.transform.rotation + 1) % 360
        
        renderer.update(0)

        myClock.tick(60) # 60 fps :)
    renderer.shutdown()
