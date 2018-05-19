import pygame


class Player:
    def __init__(self, x, y, hp, atk):
        self.__hp = hp
        self.__atk = atk
        self.__x = x
        self.__y = y

        
    def update(self,dt):
        pass
    
    def render(self,screen):
        pygame.draw.rect(screen,(0,255,0),self.rect)
        pygame.draw.rect(screen,(0,0,0),self.rect,2)



    def handleInput(self,key):
        #determine what to do based on keypress
        #arrow keys to move, z to fire
        pass

    def getRect(self):
        return pygame.Rect(self.__x,self.__y,50,50)
    
    def __fire(self,direction):
        #spawn a projectile with velocity in direction
        pass
        
    def __move(self,direction):
        self.__x += direction[0]
        self.__y += direction[1]
        
    
