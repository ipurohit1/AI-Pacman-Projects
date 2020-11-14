# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"


    frontier = util.Stack() # initialize frontier as stack 
    print(problem.getStartState())
    startLocation = problem.getStartState()
    initial_node = (startLocation, []) # tuple of state and path taken to get there 
    frontier.push(initial_node) # list of frontier, should be a queue 
    explored = []

    while True: 
        if frontier.isEmpty(): return False
        
        current_node = frontier.pop() # current_node is a tuple with position and path 
        explored.append(current_node[0])
        
        if problem.isGoalState(current_node[0]): 
            print("Finished")
            return current_node[1] # return the current position and path

        successors = problem.getSuccessors(current_node[0])
        for action in successors:
            # result = [i for i, v in enumerate(frontier.list) if v[0] == action[0]]
            if action[0] not in explored: 
                frontier.push( (action[0], current_node[1] + [action[1]])) # push tuple of action (new position) and path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue() # initialize frontier as queue 
    initial_node = (problem.getStartState(), []) # tuple of state and path taken to get there 
    frontier.push(initial_node) # list of frontier, should be a queue 
    explored = []

    while True: 
        if frontier.isEmpty(): return False
        
        current_node = frontier.pop() # current_node is a tuple with position and path 
        explored.append(current_node[0])
        
        if problem.isGoalState(current_node[0]): 
            return current_node[1] # return the current position and path

        successors = problem.getSuccessors(current_node[0])
        for action in successors:
            result = [i for i, v in enumerate(frontier.list) if v[0] == action[0]]
            if action[0] not in explored and result == []: 
                explored.append(action[0])
                frontier.push( (action[0], current_node[1] + [action[1]])) # push tuple of action (new position) and path


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    frontier = util.PriorityQueue() # initialize frontier as queue 
    initial_node = (problem.getStartState(), [], 0) # tuple of state and path taken to get there 
    frontier.push(initial_node, 0) # list of frontier, should be a queue 
    explored = []

    while True: 
        if frontier.isEmpty(): return None
        
        current_node = frontier.pop() # current_node is a tuple with position, path, and cost 
  
        if problem.isGoalState(current_node[0]): 
            print("Finished")
            return current_node[1] # return the current position and path

        if current_node[0] not in explored:
            explored.append(current_node[0]) # add node to explored 

            successors = problem.getSuccessors(current_node[0])
            for action in successors:
                if action[0] not in explored:
                    next_cost = current_node[2] + action[2] # initialize the cost using the cost so far and the cost of new successor 
                    next_node = (action[0], current_node[1] + [action[1]], next_cost)
                    result = [i for i, v in enumerate(frontier.heap) if v[0] == action[0]]

                    if result == []: # if frontier does not contain node with successor state
                        frontier.push(next_node, next_cost)
                    else: # else use the update function to update the cost
                        frontier.update(next_node, next_cost) # push tuple of next_node ((state, path, cost), priority)
                   
                    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() # initialize frontier as queue 
    initial_node = (problem.getStartState(), [], 0) # tuple of state and path taken to get there 
    frontier.push(initial_node, 0) # list of frontier, should be a queue 
    explored = []

    while True: 
        if frontier.isEmpty(): return None
        
        current_node = frontier.pop() # current_node is a tuple with position, path, and cost 
  
        if problem.isGoalState(current_node[0]): 
            print("Finished")
            return current_node[1] # return the current position and path

        if current_node[0] not in explored:
            explored.append(current_node[0]) # add node to explored 

            successors = problem.getSuccessors(current_node[0])
            for action in successors:
                result = [i for i, v in enumerate(frontier.heap) if v[0] == action[0]]

                if action[0] not in explored and result == []:
                    next_cost = current_node[2] + action[2]
                    next_node = (action[0], current_node[1] + [action[1]], next_cost)
                    frontier.push(next_node, next_cost + heuristic(action[0], problem))
                    # if result == []: # if frontier does not contain node with successor state
                        
                    # else: # else use the update function to update the cost
                    #     frontier.update(next_node, next_cost) # push tuple of next_node ((state, path, cost), priority)
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
