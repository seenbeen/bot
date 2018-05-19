

class Spawner:
    def __init__(self, delay, gameState):
        self.__timeLast = 0
        self.__gameSections = []
        self.__delay = delay
        self.__gameState = gameState
        self.__spawning = True

        
    #A section is defined as a list of enemies to spawn in order
    def loadSection(self, enemyData, sectionType):
        self.__gameSections.append([enemyData, sectionType])
        
    def __spawn(self,enemy):
        self.__gameState.addObject(enemy)
        
        
    def update(self,dt): # gameSections = [[[enemy,enemy,enemy],"rapid"], [[enemy,enemy,enemy],"continuous"]]
        """
        todo: spawn multiple enemies at a time
        """
        self.__timeLast = self.__timeLast + dt
        if (self.__spawning):
            if (self.__timeLast >= self.__delay):
                print "spawnedEnemy"
                self.__spawn(self.__gameSections[0][0].pop(0))
                self.__timeLast = 0
                
            if (len(self.__gameSections[0][0]) <= 0):
                self.__gameSections.pop(0)
                if (len(self.__gameSections) <= 0):
                    print "All enemies spawned"
                    self.__spawning = False
        
            