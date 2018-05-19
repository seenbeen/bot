import pygame._view #required for py2exe

import pygame

running = True

screen = pygame.display.set_mode((720, 900))

while running:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False
    mx,my =  pygame.mouse.get_pos()

    screen.fill((0,0,0))

    pygame.draw.rect(screen,(0,255,0),(mx-50,my-50,100,100))
    
    pygame.display.flip()

pygame.quit()

