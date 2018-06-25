"""Singleton class used to convert other classes into singletons"""
class Singleton:
    
    """Call this method on a class you wish to turn into a singleton"""
    @staticmethod
    def transformToSingleton(className):

        """Initializes the singleton, calls __init__ with any passed arguments on the singleton's class"""
        @classmethod
        def initialize(cls, *args):
            if (cls.__instance == None):
                cls.__instance = cls(*args)
            else:
                raise Exception("Singleton is already initialized(%s)"%cls.__name__)
            
        """Removes the singleton instance and calls del on the class"""
        @classmethod    
        def shutdown(cls):
            if (cls.__instance != None):
                del cls.__instance
                cls.__instance = None
            else:
                raise Exception("Singleton does not exist and is being shut down(%s)"%cls.__name__)
            
        """returns the instance of a singleton"""    
        @classmethod
        def instance(cls):
            if (cls.__instance == None):
                raise Exception("Singleton has not been initialized(%s)"%cls.__name__)
            return cls.__instance
        
        try:
            if (className.initialize != None):
                raise Exception("%s is already a singleton or has a static initialize method"%className.__name__)
        except AttributeError:
            pass
        
        className.initialize = initialize
        className.shutdown = shutdown
        className.instance = instance
        className.__instance = None

