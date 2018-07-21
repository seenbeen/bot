import time, sys
import pygame
from bot_framework.bot_GOSS import *

class TestGameApp(GameAppImpl):
    def initialize(self):
        self.shutdownCounter = 0
        dtA = DeltaTimePrinter("DeltaTimePrinter A")
        dtB = DeltaTimePrinter("DeltaTimePrinter B")
        self.gameObj = GameObject([dtA, dtB], "DeltaTimePrinterObject")
        GameApplication.instance().addObject(self.gameObj)
        GameApplication.instance().removeObject(self.gameObj)
        self.gameObj.removeComponent(dtA)
        self.gameObj.addComponent(dtA)
        GameApplication.instance().addObject(self.gameObj)
        
        try:
            GameApplication.instance().getGameObject("DeltaTimePrinterObject")
            raise Exception("DeltaTimePrinterObject should not exist before pump")
        except:
            pass

    def shutdown(self):
        print "Shutting Down GameAppImpl"

    def update(self, deltaTime):
        self.shutdownCounter+=deltaTime
        if self.shutdownCounter > 2:
            self.gameObj.destroy()
            GameApplication.instance().quitApp()
            
    def lateUpdate(self):
        pass

class DeltaTimePrinter(GameObjectComponent):
    def __init__(self, name):
        self.counter = 0.0
        super(DeltaTimePrinter, self).__init__(name)

    def onUpdate(self, dt):
        self.counter += dt
        if self.counter >= 1.0:
            print "I counted to 1"
            self.counter -= 1.0

    def onLateUpdate(self):
        pass

    def onEnter(self):
        print "%s onEnter" % self.getName()

    def onExit(self):
        print "%s onExit" % self.getName()

    def onBind(self):
        print "%s onBind" % self.getName()
        assert self.getParent().getName() == "DeltaTimePrinterObject", "Parent is incorrect for component"

    def onUnbind(self):
        print "%s onUnbind" % self.getName()

def run():
    GameApplication.initialize(TestGameApp)

    GameApplication.instance().run()

    GameApplication.shutdown()

