import pygame._view #required for py2exe
import pygame
from bot_framework.bot_inputmanager import InputManager

running = True

screen = pygame.display.set_mode((720, 900))


InputManager.initInstance()


while running:
    
    InputManager.getInstance().update(0)
    
    if InputManager.getInstance().getEvent(pygame.QUIT):
        running = False
        
    mx =  InputManager.getInstance().getMouseCoords().x
    my =  InputManager.getInstance().getMouseCoords().y
    
    screen.fill((0,0,0))

    pygame.draw.rect(screen,(0,255,0),(mx-50,my-50,100,100))
    
    pygame.display.flip()

pygame.quit()

InputManager().shutdownInstance()