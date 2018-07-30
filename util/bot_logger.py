from util.pattern.bot_singleton import Singleton

class Logger():
    def __init__(self):
        self.__file = open("log.txt", "w")
        
    def log(self, line):
        self.__file.write(line)
        self.__file.write("\n")
    
    def __del__(self):
        self.__file.close()
        
Singleton.transformToSingleton(Logger)
        