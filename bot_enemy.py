import pygame


class Enemy:
    def __init__(self, x, y, hp, atk):
        self._hp = hp
        self._atk = atk
        self._x = x
        self._y = y



    def update(self,dt):
        pass
        
    def render(self, screen):
        pygame.draw.rect(screen,(255,0,0),self.getRect())
        pygame.draw.rect(screen,(0,0,0),self.getRect(),2)

        
    def __fire(self, direction):
        pass
    
    def getRect(self):
        return pygame.Rect(self._x,self._y,50,50)
        
        
        
class runDown(Enemy):
    
    def update(self,dt):
        self._y += 1.0*dt
