from bot_gamestatmanager import *
from bot_inputmanager import *
import pygame

class Component(object):
    '''
    classdocs
    '''
    
    def __init__(self, gameObject):
        self.gameObject = gameObject
    
    def update(self, dt):
        
        raise Exception('Error, %s must define a update method'%self.__class__.__name__)
    
    def lateUpdate(self, dt):
        
        raise Exception('Error, %s must define a late update method'%self.__class__.__name__)
    
    
    
class BoxRenderComponent(Component):
    
    def __init__(self, gameObject, color):
        super(BoxRenderComponent, self).__init__(gameObject)
        self.color = color

    def update(self, dt):
        pygame.draw.rect(StateManager.screen, self.color, self.getRect())
        pygame.draw.rect(StateManager.screen, (0,0,0), self.getRect(), 2)
    
    def getRect(self):
        return pygame.Rect(self.gameObject.x, self.gameObject.y, 50, 50)
        

class CharMovementComponent(Component):
    def __init__(self, gameObject, up, down, left, right, speed):
        super(CharMovementComponent, self).__init__(gameObject)
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.speed = speed
    
    def update(self, dt):
        if InputManager.getKey(self.up):
            self.gameObject.translate(0, -self.speed*dt)
            
        if InputManager.getKey(self.down):
            self.gameObject.translate(0, self.speed*dt)
            
        if InputManager.getKey(self.left):
            self.gameObject.translate(-self.speed*dt, 0)
            
        if InputManager.getKey(self.right):
            self.gameObject.translate(self.speed*dt, 0)