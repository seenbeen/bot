import pygame,sys
from Gamestate import *
from Player import *
from Spawner import *
import Enemy
import time




size = (width, height) = 1280, 720
screen = pygame.display.set_mode(size)





myGameState = GameState()

mySpawner = Spawner(100.0, myGameState)

myEnemy = Enemy.runDown(20,50,5,5)
myEnemy2 = Enemy.runDown(50,50,5,5)
myEnemy3 = Enemy.runDown(70,50,5,5)

enemies = [myEnemy,myEnemy2,myEnemy3]

mySpawner.loadSection([myEnemy,myEnemy2,myEnemy3], "same")




myGameState.addObject(mySpawner)

start = time.time()

running = True
while running:
    screen.fill((0,0,0))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit(0)


    deltaTime = time.time() - start
            
    myGameState.update(deltaTime)
    for enemy in enemies:
        enemy.render(screen)
    pygame.display.flip()
