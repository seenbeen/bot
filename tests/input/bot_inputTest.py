import pygame
from bot_framework.bot_inputmanager import InputManager, InputListener

FakeEventA = pygame.USEREVENT+1
FakeEventB = pygame.USEREVENT+2
FakeEventC = pygame.USEREVENT+3

class blockA(InputListener):
    SET = 0
    RECEIVE = 0
    def eventImpl(self, evt):
        blockA.RECEIVE += 1
        if (evt.type==FakeEventA):
            print "I received A and blocked"
            blockA.SET += 1
            return True
        return False

class passB(InputListener):
    SET = 0
    RECEIVE = 0
    def eventImpl(self, evt):
        passB.RECEIVE += 1
        if (evt.type==FakeEventB):
            print "I received B and did not block"
            passB.SET += 1
            return False
        return False

class passAny(InputListener):
    SET = 0
    def eventImpl(self, evt):
        print "I received %s and did not block"%evt.type
        passAny.SET += 1
        return False

def run():
    pygame.init()
    
    InputManager.initialize()
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(FakeEventA))
    pygame.event.post(pygame.event.Event(FakeEventB))
    pygame.event.post(pygame.event.Event(FakeEventC))

    A = blockA()
    B = passB()
    C = passAny()

    A.registerManager(0)
    A.addListener(B)
    A.addListener(C)

    InputManager.instance().update(0)

    assert blockA.SET == 1 and blockA.RECEIVE == 3, "BlockA event was called an incorrect number of times"
    assert passB.SET == 1 and passB.RECEIVE == 2, "passB event was called an incorrect number of times"
    assert passAny.SET == 2, "passAny event was called an incorrect number of times"

