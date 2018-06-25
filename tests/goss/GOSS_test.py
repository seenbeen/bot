import time, sys
import pygame
from bot_framework.bot_inputmanager import *
from bot_framework.bot_GOSS import *

class TestGameApp(GameAppImpl):
    def initialize(self):
        print "Initializing Game Subsystems"
        size = (width, height) = 1280, 720
        self.screen = pygame.display.set_mode(size)
        InputManager.initialize()
        
        printer = DeltaTimePrinter("DeltaTimePrinter")
        GameApplication.instance().addObject(GameObject([printer],"DeltaTimePrinterObject"))
        
        try:
            GameApplication.instance().getGameObject("DeltaTimePrinterObject")
        except Exception:
            pass
        else:
            raise Exception("DeltaTimePrinterObject should not exist before pump")

    def shutdown(self):
        InputManager.shutdown()
        pygame.quit()
        print "Shutting Down Game Subsystems"

    def update(self, deltaTime):
        self.screen.fill((0,0,0))

        InputManager.instance().update(deltaTime)

        if InputManager.instance().getEvent(pygame.QUIT):
            GameApplication.instance().quit()

    def lateUpdate(self):
        pygame.display.flip()

class DeltaTimePrinter(ScriptComponent):
    def __init__(self, name):
        self.counter = 0.0
        super(DeltaTimePrinter, self).__init__(name)

    def update(self, dt):
        self.counter += dt
        if self.counter >= 1.0:
            print "I counted to 1"
            self.counter -= 1.0
    def lateUpdate(self):
        pass

    def onBind(self):
        assert self.gameObjectParent.name == "DeltaTimePrinterObject", "Parent is incorrect for component"

def run():
    GameApplication.initialize(TestGameApp)

    GameApplication.instance().run()

    GameApplication.shutdown()
