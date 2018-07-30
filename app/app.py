import pygame

from util.bot_asset_util import AssetUtil
from util.bot_logger import Logger
from util.bot_math import *

from bot_framework.bot_assetManager import AssetManager
from bot_framework.bot_fsm import *
from bot_framework.bot_GOSS import *
from bot_framework.bot_inputmanager import *
from bot_framework.bot_physics import BOTPhysicsSpace
from bot_framework.bot_render import *

from player import Ship

class BOTGameAppQUITListener(InputListener):
    def __init__(self):
        self.QUIT_PRESSED = False

    def onEvent(self, evt):
        if evt.type == pygame.QUIT:
            self.QUIT_PRESSED = True
            return True
        return False

class BOTGameApp(GameAppImpl):
    __PROJECT_PATH = ""
    __ASSET_FILE = "assets/assets_list"

    __WINDOW_DIMENSIONS = (720, 900)

    # TODO: We need a logger to log what's goin on OTL

    def __initializeAssetManager(self):
        AssetManager.initialize(BOTGameApp.__PROJECT_PATH)
        assetManager = AssetManager.instance()

        # load asset callbacks
        assetManager.loadTypeCallback(".bsprite", AssetUtil.loadSpriteSheet)

        # load in assets
        assetManager.load(BOTGameApp.__ASSET_FILE)

    def __shutdownAssetManager(self):
        AssetManager.shutdown()

    def __initializePhysicsSpace(self):
        BOTPhysicsSpace.initialize()

    def __shutdownPhysicsSpace(self):
        BOTPhysicsSpace.shutdown()

    def __initializeRenderer(self):
        BOTRenderer.initialize(*BOTGameApp.__WINDOW_DIMENSIONS, windowTitle="BOT v0.1!")
 
    def __shutdownRenderer(self):
        BOTRenderer.shutdown()

    def __initializeInputManager(self):
        InputManager.initialize()
        InputManager.instance().setupPriority(["QUIT_PRIORITY", "UI", "GAME"])
        
    def __shutdownInputManager(self):
        InputManager.shutdown()
        
    def __initializeLogger(self):
        Logger.initialize()
    
    def __shutdownLogger(self):
        Logger.shutdown()
        

    def initialize(self):
        self.__initializeLogger()
        self.__initializeAssetManager()
        self.__initializePhysicsSpace()
        self.__initializeRenderer()
        self.__initializeInputManager()
        self.__fsm = BOTGameAppFSM(self)

    def shutdown(self):
        
        self.__shutdownInputManager()
        self.__shutdownRenderer()
        self.__shutdownPhysicsSpace()
        self.__shutdownAssetManager()
        self.__shutdownLogger()
        

    def update(self, deltaTime):
        InputManager.instance().update(deltaTime)
        BOTPhysicsSpace.instance().update(deltaTime)
        BOTRenderer.instance().update(deltaTime)
        self.__fsm.update(deltaTime)

    def lateUpdate(self):
        InputManager.instance().lateUpdate()
        BOTPhysicsSpace.instance().lateUpdate()
        self.__fsm.lateUpdate()

class BOTGameAppFSM(BOTFSM):
    # Menu
    @staticmethod
    def __MenuInit(self):
        windowDims = Vector2(*BOTRenderer.instance().getScreenDimensions())

        # create Scenes
        self.gameScene = BOTScene("BOTRenderer::MenuGameScene")
        self.uiScene = BOTScene("BOTRenderer::MenuUIScene")

        # create cameras
        self.gameCamera = BOTCamera(*(windowDims / 4).toIntTuple(),
                                    name="BOTRenderer::MenuGameCamera")
        self.uiCamera = BOTCamera(*windowDims.toIntTuple(),
                                  name="BOTRenderer::MenuUICamera")
        self.uiCamera.transform.position += windowDims * Vector2(0.5, 0)

        # create viewports
        self.gameViewport = BOTViewport(*windowDims.toIntTuple(),
                                        name="BOTRenderer::MenuGameViewport")
        self.uiViewport = BOTViewport(*windowDims.toIntTuple(),
                                      name="BOTRenderer::MenuUIViewport")

        # create compositing
        self.gameCameraCompositor = BOTCameraCompositor(self.gameScene.getName(),
                                                        self.gameCamera.getName(),
                                                        self.gameViewport.getName(),
                                                        BOTCompositingCache.getScreenKey())
        self.uiCameraCompositor = BOTCameraCompositor(self.uiScene.getName(),
                                                      self.uiCamera.getName(),
                                                      self.uiViewport.getName(),
                                                      BOTCompositingCache.getScreenKey())

        # set up inputs for quitting
        self.quitListener = BOTGameAppQUITListener()
        self.quitListener.registerToManager("QUIT_PRIORITY")

        # now for some objects...
        self.shipA = Ship(self.gameScene.getName(), "BOTGame::ShipA")

    @staticmethod
    def __MenuTransitionFrom(self, fromState):
        renderer = BOTRenderer.instance()
        renderer.registerScene(self.gameScene)
        renderer.registerScene(self.uiScene)
        renderer.registerCamera(self.gameCamera)
        renderer.registerCamera(self.uiCamera)
        renderer.registerViewport(self.gameViewport)
        renderer.registerViewport(self.uiViewport)
        renderer.chainCompositor(self.gameCameraCompositor)
        renderer.chainCompositor(self.uiCameraCompositor)

        GameApplication.instance().addObject(self.shipA)

    @staticmethod
    def __MenuTransitionTo(self, toState):
        # remove stuff in opposite order to adding
        GameApplication.instance().removeObject(self.shipA)
        # temporary hack... we need to flush removes before renderer wipes
        GameApplication.instance().pump()

        renderer = BOTRenderer.instance()
        renderer.clearCompositingChain()
        renderer.unregisterViewport(self.uiViewport)
        renderer.unregisterViewport(self.gameViewport)
        renderer.unregisterCamera(self.uiCamera)
        renderer.unregisterCamera(self.gameCamera)
        renderer.unregisterScene(self.uiScene)
        renderer.unregisterScene(self.gameScene)

    @staticmethod
    def __MenuUpdate(self, deltaTime):
        if self.quitListener.QUIT_PRESSED:
            self.transitionToState("Quit")

    @staticmethod
    def __MenuLateUpdate(self):
        pass

    # Game
    @staticmethod
    def __GameInit(self):
        pass

    @staticmethod
    def __GameTransitionFrom(self, fromState):
        pass

    @staticmethod
    def __GameTransitionTo(self, toState):
        pass

    @staticmethod
    def __GameUpdate(self, deltaTime):
        pass

    @staticmethod
    def __GameLateUpdate(self):
        pass

    # Quit
    @staticmethod
    def __QuitInit(self):
        pass

    @staticmethod
    def __QuitTransitionFrom(self, fromState):
        pass

    @staticmethod
    def __QuitTransitionTo(self, toState):
        pass

    @staticmethod
    def __QuitUpdate(self, deltaTime):
        GameApplication.instance().quitApp()

    @staticmethod
    def __QuitLateUpdate(self):
        pass

    def FSMInit(self):
        states = [
                    {
                        "name" : "Menu",
                        "methods" : {
                            "init" : self.__MenuInit,
                            "transitionFrom" : self.__MenuTransitionFrom,
                            "transitionTo" : self.__MenuTransitionTo,
                            "update" : self.__MenuUpdate,
                            "lateUpdate" : self.__MenuLateUpdate,
                        }
                    },
                    {
                        "name" : "Game",
                        "methods" : {
                            "init" : self.__GameInit,
                            "transitionFrom" : self.__GameTransitionFrom,
                            "transitionTo" : self.__GameTransitionTo,
                            "update" : self.__GameUpdate,
                            "lateUpdate" : self.__GameLateUpdate,
                        }
                    },
                    {
                        "name" : "Quit",
                        "methods" : {
                            "init" : self.__QuitInit,
                            "transitionFrom" : self.__QuitTransitionFrom,
                            "transitionTo" : self.__QuitTransitionTo,
                            "update" : self.__QuitUpdate,
                            "lateUpdate" : self.__QuitLateUpdate,
                        }
                    }
                ]
        initState = "Menu"
        return [initState, states]
