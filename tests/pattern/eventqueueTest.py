from util.pattern.bot_eventqueue import EventQueue

def run():
    class Foo:
        MAGI = "MAGIC"
        PHYS = "PHYSICAL"
        HEAL = "HEALING"

        def __init__(self, val):
            self.__hp = val

        def applyDeltaHP(self, delta, kind):
            print "MODIFY HP, kind = %s, delta= %i"%(kind, delta)
            self.__hp += delta

        def setHP(self, val, kind):
            print "SETTING HP, kind = %s, val = %i"%(kind, val)
            self.__hp = val

        def dankTheMemes(self):
            print "Danking the memes always comes first :^)"

        def getHP(self):
            return self.__hp

    # wrap in a module private function to not pollute global namespace
    def __makeFooAQueue():
        QUEUED_METHODS = [Foo.applyDeltaHP, Foo.setHP, Foo.dankTheMemes]

        DANK_METH = Foo.dankTheMemes.__name__
        DELT_HP_METH = Foo.applyDeltaHP.__name__
        SET_HP_METH = Foo.setHP.__name__

        KIND_ORDER = {Foo.MAGI : 0, Foo.PHYS : 1, Foo.HEAL : 2}
        METHOD_ORDER = {DANK_METH : 0, DELT_HP_METH: 1, SET_HP_METH : 2}

        def pumpCompare(eventA, eventB):
            # NOTE: This is a relatively simple example; the comparator
            # can get a lot more complex, but we'll say setHP calls get the last say
            # and healing always comes after physical, after magic damage

            # dank first, others later :)
            if eventA.name != eventB.name:
                return (METHOD_ORDER[eventA.name] - METHOD_ORDER[eventB.name])
            
            if eventA.name == DANK_METH:
                return 0 # dank methods are all equally dank
            elif eventA.name == DELT_HP_METH:
                # order by kind priorities
                return (KIND_ORDER[eventA.argsDict["kind"]] -
                        KIND_ORDER[eventB.argsDict["kind"]])
            elif eventA.name == SET_HP_METH:
                # order againby kind priorities
                return (KIND_ORDER[eventA.argsDict["kind"]] -
                        KIND_ORDER[eventB.argsDict["kind"]])
            else:
                raise Exception("Unexpected method %s being pumped!"%eventA.name)

        EventQueue.enQueueify(Foo, QUEUED_METHODS, pumpCompare)

    __makeFooAQueue()

    for i in range(3):
        print "Create"
        f = Foo(42)

        print "Delayed Calls"

        f.setHP(1337, Foo.HEAL)
        f.setHP(100, Foo.MAGI)
        f.applyDeltaHP(-2, Foo.MAGI)
        f.dankTheMemes()
        f.dankTheMemes()

        print "HP is %i"%f.getHP()

        print "Pump Call"
        f.pump()

        print "HP is %i"%f.getHP()
