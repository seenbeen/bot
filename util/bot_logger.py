from util.pattern.bot_singleton import Singleton

class Logger():
    def __init__(self):
        self.__file = open("log.txt", "w")
        self.__frame = 0
        
    def log(self, line):
        self.__file.write(str(self.__frame) + ":" + line)
        self.__file.write("\n")
        
    def tick(self):
        self.__frame += 1
        
    def __del__(self):
        self.__file.close()
        
Singleton.transformToSingleton(Logger)
        