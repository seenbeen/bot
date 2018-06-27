from bot.bot_game.bot_gameobject import *

class Spawner(Component):
    def __init__(self, delay, gameState, gameObjectParent):
        raise Exception("Deprecated")
        self.__timeLast = 0
        self.__gameSections = []
        self.__delay = delay
        self.__gameState = gameState
        self.__spawning = True

        self.__toSpawn = None
        super().__init__(gameObjectParent)
    #A section is defined as a list of enemies to spawn in order
    def loadSection(self, enemyData, sectionType):
        self.__gameSections.append([enemyData, sectionType])
        
    def __spawn(self):
        self.__gameState.addObject(self.__toSpawn, "Enemy")
        
    def update(self,dt): # gameSections = [[[enemy,enemy,enemy],"rapid"], [[enemy,enemy,enemy],"continuous"]]
        """
        todo: spawn multiple enemies at a time
        """
        self.__timeLast = self.__timeLast + dt
        if (self.__spawning):
            if (self.__timeLast >= self.__delay):
                self.__toSpawn = self.__gameSections[0][0].pop(0)
                self.__timeLast = 0
                
            if (len(self.__gameSections[0][0]) <= 0):
                self.__gameSections.pop(0)
                if (len(self.__gameSections) <= 0):
                    self.__spawning = False
        
    def lateUpdate(self, dt):
        if (self.__toSpawn != None):
            self.__spawn()
