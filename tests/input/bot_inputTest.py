import pygame
from bot_framework.bot_inputmanager import InputManager, InputListener

FakeEventA = pygame.USEREVENT + 1
FakeEventB = pygame.USEREVENT + 2
FakeEventC = pygame.USEREVENT + 3

class blockA(InputListener):
    set = 0
    receive = 0
    def onEvent(self, evt):
        blockA.receive += 1
        if (evt.type==FakeEventA):
            print "I received A and blocked"
            blockA.set += 1
            return True
        return False

class passB(InputListener):
    set = 0
    receive = 0
    def onEvent(self, evt):
        passB.receive += 1
        if (evt.type==FakeEventB):
            print "I received B and did not block"
            passB.set += 1
            return False
        return False

class passAny(InputListener):
    set = 0
    def onEvent(self, evt):
        print "I received %s and did not block"%evt.type
        passAny.set += 1
        return False

def run():
    pygame.init()
    
    InputManager.initialize()
    InputManager.instance().setupPriority([InputManager.UI, InputManager.MENU, InputManager.GAMEOBJECT])
    
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(FakeEventA))
    pygame.event.post(pygame.event.Event(FakeEventB))
    pygame.event.post(pygame.event.Event(FakeEventC))

    A = blockA()
    B = passB()
    C = passAny()

    A.registerManager(InputManager.MENU)
    A.addListener(B)
    A.addListener(C)

    InputManager.instance().update(0)

    assert blockA.set == 1 and blockA.receive == 3, "BlockA event was called an incorrect number of times"
    assert passB.set == 1 and passB.receive == 2, "passB event was called an incorrect number of times"
    assert passAny.set == 2, "passAny event was called an incorrect number of times"

