

class StateManager:
    
    currentGameState = None
    allGameStates = { }
    screen = None
    
    @staticmethod
    def setState(newState):
        StateManager.currentGameState = StateManager.allGameStates[newState]
        #print __currentGameState
        
    @staticmethod   
    def addState(newState, stateName):
        StateManager.allGameStates[stateName] = newState
        
    @staticmethod    
    def currentState():
        return StateManager.currentGameState    