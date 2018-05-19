

class GameState:
    def __init__(self):
        self.__gameObjects = []
        
    def update(self, dt):
        for obj in self.__gameObjects:
            obj.update(dt)


    def addObject(self, obj):
        self.__gameObjects.append(obj)

    def removeObject(self, obj):
        self.__gameObjects.remove(obj)

        
    
