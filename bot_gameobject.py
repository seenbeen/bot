
class GameObject(object):
    '''
    classdocs
    '''
    

    def __init__(self, x, y):
        '''
        Constructor
        '''
        
        self.__components = {}
        self.x = x
        self.y = y
        
    def addComponent(self, comp, name):
        self.__components[name] = comp
        
    def removeComponent(self, name):
        #TODO
        del self.__components[name]
    
    def update(self, dt):
        for comp in self.__components:
            self.__components[comp].update(dt)
            
    def lateUpdate(self, dt):
        for comp in self.__components:
            self.__components[comp].lateUpdate(dt)
            
    def destroy(self):
        #TODO
        pass
    
    def translate(self, x, y):
        self.x += x
        self.y += y