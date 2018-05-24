

class GameState:
    def __init__(self):
        self.__gameObjects = { }
        
    def update(self, dt):
        for obj in self.__gameObjects:
            self.__gameObjects[obj].update(dt)

    def lateUpdate(self,dt):
        for obj in self.__gameObjects:
            self.__gameObjects[obj].lateUpdate(dt)
            
    def addObject(self, obj, name):
        self.__gameObjects[name] = obj

    def removeObject(self, name):
        del self.__gameObjects[name]

        
    
