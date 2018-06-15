import pygame,sys
from bot_gamestate import *
from bot_player import *
from bot_spawner import *
from bot_gamestatmanager import *
from bot_inputmanager import *
from bot_gameobject import *
import bot_component
import bot_enemy
import time




size = (width, height) = 1280, 720
screen = pygame.display.set_mode(size)





StateManager.addState(GameState(), "main") 
StateManager.setState("main")

#mySpawner = Spawner(100.0, StateManager.currentState())





#StateManager.currentState().addObject(mySpawner, "Spawner")

player1 = GameObject(50,50)
player2 = GameObject(100,50)

player1.addComponent(bot_component.BoxRenderComponent(player1, (255,0,0)), "renderer")
player2.addComponent(bot_component.BoxRenderComponent(player2, (255,0,0)), "renderer")

player1.addComponent(bot_component.CharMovementComponent(player1,ord('w'),ord('s'),ord('a'),ord('d'), 100.0), "move")
player2.addComponent(bot_component.CharMovementComponent(player2,ord('i'),ord('k'),ord('j'),ord('l'), 100.0), "move")


StateManager.currentState().addObject(player1, "player1")
StateManager.currentState().addObject(player2, "player2")

StateManager.screen = screen

start = time.time()
currentTime = start
running = True


while running:
    currentTime = time.time()
    
    deltaTime = currentTime - start 
    
    screen.fill((0,0,0))
    
    InputManager.resetEvents()
    InputManager.setEvents(pygame.event.get())
    InputManager.setKeys(pygame.key.get_pressed())
    
    if InputManager.getKey(ord('q')):
        running = False
        pygame.quit()
        sys.exit(0)
    
      
    StateManager.currentState().update(deltaTime)
    
        
    pygame.display.flip()
    start = currentTime
