import pygame._view #required for py2exe
import pygame
from bot_framework.bot_inputmanager import InputManager

running = True

screen = pygame.display.set_mode((720, 900))


myInputs = InputManager()

while running:
    
    myInputs.update(0)
    
    if myInputs.getEvent(pygame.QUIT):
        running = False
    mx,my =  myInputs.getMouseCoords()

    screen.fill((0,0,0))

    pygame.draw.rect(screen,(0,255,0),(mx-50,my-50,100,100))
    
    pygame.display.flip()

pygame.quit()

