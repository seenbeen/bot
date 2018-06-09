from util.pattern.bot_singleton import Singleton
class tester:
    x = None
    d = False
    def __init__(self, x):
        tester.x = x
        
    def __del__(self):
        tester.d = True
        
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
    
    assert tester.d == True, "__del__ test failed"
    
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
