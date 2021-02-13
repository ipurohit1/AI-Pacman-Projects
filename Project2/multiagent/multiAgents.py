# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action) # gets some successor game state
        newPos = successorGameState.getPacmanPosition() # gets the pos of the state
        newFood = successorGameState.getFood() # gets the remaining food
        newGhostStates = successorGameState.getGhostStates() 
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # number of moves that the ghosts will still be scared

        "*** YOUR CODE HERE ***"
        # print('new pos: ', newPos)
        # print('new ghost states', newGhostStates[0])
        # print('new food ', newFood.asList())
        # print('scared times ', newScaredTimes)

        # currentPos = list(successorGameState.getPacmanPosition())
        # distance = -1000000

        # foodList = currentGameState.getFood().asList()

        # for food in foodList:

        min_food_distance = 1000000
        min_new_food_distance = 1000000

        oldPos = currentGameState.getPacmanPosition()

        food_list = currentGameState.getFood().asList() 

        if food_list: 
            for food in food_list: 
                min_food_distance = min(min_food_distance, manhattanDistance(oldPos, food)) 
                min_new_food_distance = min(min_new_food_distance, manhattanDistance(newPos, food))
    
        else: 
            min_food_distance = 0
            min_new_food_distance = 0 

        # if positive, newer position is closer to food (more desirable) 
        # if negative, older position is closer to food (less desirable)
        distance = min_food_distance - min_new_food_distance
        
        
    
        return successorGameState.getScore() + distance


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 1)[1]

    
    # given a game state, determines the max value that can be obtained in the game
    # and what action leads to that value (pacman strategy)
    def maxValue(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth > self.depth: 
            return self.evaluationFunction(gameState), None

        negative_value = -1000000

        for action in gameState.getLegalActions(0): 
            min_value = self.minValue(gameState.generateSuccessor(0, action), 1, depth)[0]
            # Keeping track of the max value seen so far and which action led to it 
            if min_value > negative_value: 
                negative_value = min_value
                value = min_value, action

        return value
    
    # given a game state, determines the min value that can be obtained in the game (ghost strategy)
    def minValue(self, gameState, agentIndex, depth): 
        if gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState), None


        pos_value = 1000000

        # the calculation for the last ghost, should increase depth 
        if agentIndex == gameState.getNumAgents() -1: 
            for action in gameState.getLegalActions(agentIndex): 
                min_value = self.maxValue(gameState.generateSuccessor(agentIndex, action), depth + 1)[0]
                # update lowest value seen so far 
                if min_value < pos_value: 
                    pos_value = min_value
                    value = min_value, action
        else: 
            for action in gameState.getLegalActions(agentIndex):
                min_value =  self.minValue(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth)[0]
                # update lowest value seen so far 
                if min_value < pos_value: 
                    pos_value = min_value
                    value = min_value, action

        return value          


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        # call maxValue, but return just the action (index 1 of tuple)
        return self.maxValue(gameState, 1, -100000, 100000)[1]


    def maxValue(self, gameState, depth, alpha, beta): 

        # check for win, lose, or depth constraint 
        if gameState.isWin() or gameState.isLose() or depth > self.depth: 
            return self.evaluationFunction(gameState), None

        # Pick some arbitrary small negative value to start 
        value_so_far = -1000000

        for action in gameState.getLegalActions(0): 
            successor_state = gameState.generateSuccessor(0, action)
            max_value = self.minValue(successor_state, 1, depth, alpha, beta)[0]

            # update highest value so far and the return_value to include the corresponding action 
            if max_value > value_so_far:
                value_so_far = max_value
                return_value = max_value, action 
            # the highest value so far is greater than beta, return it 
            if value_so_far > beta: 
                return return_value
            
            # update alpha value 
            alpha = max(alpha, value_so_far)

        return return_value
            

    def minValue(self, gameState, agentIndex, depth, alpha, beta): 
        if gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState), None

        # Pick some arbitrary large positive value to start 
        value_so_far = 100000
        value = 0 
     
        for action in gameState.getLegalActions(agentIndex):

            # action for the last ghost 
            if agentIndex == gameState.getNumAgents() - 1: 
                value = self.maxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, alpha, beta)[0]
            # ghosts other than the last one 
            else: 
                value = self.minValue(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth, alpha, beta)[0]

            if value < value_so_far: 
                value_so_far = value 
                return_value = value, action 
            
            if value_so_far < alpha: 
                return return_value

            beta = min(value_so_far, beta)

        return return_value
                    


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 1)[1]

    def maxValue(self, gameState, depth): 

        if gameState.isWin() or gameState.isLose() or depth > self.depth: 
            return self.evaluationFunction(gameState), None

        value_so_far = -1000000 

        for action in gameState.getLegalActions(0): 
            expected_value = self.expectedValue(gameState.generateSuccessor(0, action), 1, depth)[0]
            # Keeping track of the max value seen so far and which action led to it 
            if expected_value > value_so_far: 
                value_so_far = expected_value
                value = expected_value, action

        return value
        
    def expectedValue(self, gameState, agentIndex, depth): 
        if gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState), None

        value = 0 
        for action in gameState.getLegalActions(agentIndex): 
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1: 
                value += self.maxValue(successor, depth + 1)[0]
         
            else: 
                value += self.expectedValue(successor, agentIndex + 1, depth)[0]

        value = value/len(gameState.getLegalActions(agentIndex))
        return value, None

        




def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Evaluation functipon first checks for terminal states (win or lose). If the current state isn't one of those, 
    it used the distance to the closest food item and the distance to the closest ghost and the score of the game state
    to evaluate how desirable a state is. 
    """
    "*** YOUR CODE HERE ***"

    if currentGameState.isWin(): 
        return 1000000

    if currentGameState.isLose(): 
        return -1000000

    position = currentGameState.getPacmanPosition()
    # find the closest distance to food and subtract that from score (higher distances indicate less desirable states)
    min_food_distance = 100000
    food_list = currentGameState.getFood().asList() 
    if food_list: 
        for food in food_list: 
            min_food_distance = min(min_food_distance, manhattanDistance(position, food)) 
    else: 
        min_food_distance = 0


    min_ghost_distance = 1000000
    sum_scared_time = 0
    ghost_list = currentGameState.getGhostStates()

    for ghost in ghost_list: 
        min_ghost_distance = min(min_ghost_distance, manhattanDistance(position, ghost.getPosition()))
        sum_scared_time += ghost.scaredTimer

    if sum_scared_time == 0: 
        min_ghost_distance = min_ghost_distance * -1

    # decrease magnitude of this metric, food distance should be valued more 
    min_ghost_distance = min_ghost_distance/3
  

    score = currentGameState.getScore()
    final_score = score - min_food_distance + min_ghost_distance
    return final_score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
