from util.pattern.bot_singleton import Singleton

class tester:
    x = None
    
    def __init__(self, x):
        tester.x = x
        
    @staticmethod
    def doSomething():
        print tester.x
        
def run():
    Singleton.transformToSingleton(tester)
    tester.initialize("I am a singleton")
    testInit()
    tester.instance().doSomething()
    tester.shutdown()
    testShutdown()
    
def testInit():
    try:
        tester.initialize("I shouldn't exist")
    except Exception:
        return
    raise Exception("Failed, Init called twice")

def testShutdown():
    try:
        tester.shutdown()
    except Exception:
        return
    raise Exception("Failed, shutdown called twice")
