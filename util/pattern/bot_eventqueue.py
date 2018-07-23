class EventQueue:
    '''
    On init:
        - give class an event queue.

    On specified methods, remap to a wrapped "pump" method which:
        - instead, adds call bundle to event queue
        - event queue is sorted based on the provided event comparator
        - pump method calls cannot call other pump methods to
          resolve themselves
          Eg:
              def myPumpMethod(self, you):
                  you.yourPumpMethod()

          This is illegal as calling pump surjects a pump call to which
          when its actual execution occurs is undefined

    pump is added as a method to class:
        - goes through the entire queue and pumps all methods, calling them
          as we go
    '''
    class MethodInfo:
        def __init__(self, meth, name, args):
            self.meth = meth
            self.name = meth.__name__
            self.__instance = args[0]

            self.argsDict = {}
            argCount = 1
            argLen = len(args)
            argNames = meth.im_func.func_code.co_varnames
            while argCount < argLen:
                self.argsDict[argNames[argCount]] = args[argCount]
                argCount += 1

        def call(self):
            self.meth(self.__instance, **self.argsDict)


    __ENQUEUEIFIED = "-ENQUEUEIFIED"
    __QUEUE_KEY = "-EVENT_QUEUE"
    __CALL_STACK_PUMP_METHODS = set()
    
    @staticmethod
    def __pumpifyMethod(method):
        def pumpMethod(*args):
            if method.__name__ in EventQueue.__CALL_STACK_PUMP_METHODS:
                raise Exception("Fatal: Cyclical pump attempt on method " +
                                "'%s' detected." %
                                (method.__name__))

            bundle = EventQueue.MethodInfo(method, method.__name__, args)
            args[0].__dict__[EventQueue.__QUEUE_KEY].append(bundle)
        return pumpMethod

    @staticmethod
    def enQueueify(className, methods, eventComparator):
        if EventQueue.__ENQUEUEIFIED in className.__dict__:
            raise Exception("Attempting to enqueueify class '%s' twice!"%className.__name__)

        oInit = className.__init__ if "__init__" in className.__dict__ else lambda self : None

        for m in methods:
            if type(m).__name__ not in ["instancemethod"]:
                raise Exception("Attempting to enqueueify non-instance method " +
                                "'%s' from class '%s'!"%(type(m).__name__, className.__name__)) 

            mName = m.__name__
            if mName not in className.__dict__:
                raise Exception("Attempting to enqueuify non-existent instance method " +
                                "'%s' in class '%s'!"%(m.__name__, className.__name__))

            setattr(className, mName, EventQueue.__pumpifyMethod(m))

        def __init__(self, *args):
            self.__dict__[EventQueue.__QUEUE_KEY] = []
            oInit(self, *args)

        def pump(self):
            evtQueue = self.__dict__[EventQueue.__QUEUE_KEY]
            evtQueue.sort(cmp=eventComparator)
            for x in evtQueue:
                EventQueue.__CALL_STACK_PUMP_METHODS.add(x.name)
                x.call()
                EventQueue.__CALL_STACK_PUMP_METHODS.remove(x.name)

            del evtQueue[:]

        className.__init__ = __init__
        className.pump = pump
        setattr(className, EventQueue.__ENQUEUEIFIED, True )
