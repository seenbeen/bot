


class Singleton:
    
    
    @staticmethod
    def createSingleton(className):
        
        
        @classmethod
        def initInstance(cls, *args):
            if (cls.__instance == None):
                cls.__instance = cls(*args)
            else:
                raise Exception("Singleton is already initialized(%s)"%cls.__name__)
            
        @classmethod    
        def shutdownInstance(cls):
            if (cls.__instance != None):
                cls.__instance = None
            else:
                raise Exception("Singleton does not exist and is being shut down(%s)"%cls.__name__)
            
        @classmethod
        def instance(cls):
            if (cls.__instance == None):
                raise Exception("Singleton has not been initialized(%s)"%cls.__name__)
            return cls.__instance
        
        
        className.initInstance = initInstance
        className.shutdownInstance = shutdownInstance
        className.instance = instance
        className.__instance = None