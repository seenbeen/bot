
class Singleton:
     
    @staticmethod
    def transformToSingleton(className):
        
        @classmethod
        def initialize(cls, *args):
            if (cls.__instance == None):
                cls.__instance = cls(*args)
            else:
                raise Exception("Singleton is already initialized(%s)"%cls.__name__)
            
        @classmethod    
        def shutdown(cls):
            if (cls.__instance != None):
                del cls.__instance
                cls.__instance = None
            else:
                raise Exception("Singleton does not exist and is being shut down(%s)"%cls.__name__)
            
        @classmethod
        def instance(cls):
            if (cls.__instance == None):
                raise Exception("Singleton has not been initialized(%s)"%cls.__name__)
            return cls.__instance
        
        className.initialize = initialize
        className.shutdown = shutdown
        className.instance = instance
        className.__instance = None
        