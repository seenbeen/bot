import pygame._view #required for py2exe
import pygame
from bot_framework.bot_inputmanager import InputManager
from util.pattern.bot_singleton import Singleton

running = True
screen = pygame.display.set_mode((720, 900))

InputManager.initialize()

while running:
    
    InputManager.instance().update(0)
    
    if InputManager.instance().getEvent(pygame.QUIT):
        running = False
        
    mx =  InputManager.instance().getMouseCoords().x
    my =  InputManager.instance().getMouseCoords().y
    
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,255,0),(mx-50,my-50,100,100))
    pygame.display.flip()

pygame.quit()
InputManager().shutdown()
