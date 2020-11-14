# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # run the Value Iteration formula self.iterations times 
        # self.values have the values of each state 
        # self.values = util.Counter()
        # print(self.values)
        # print(type(self.values))
        # print(type(self.mdp.getStates()[1]))

        # run loop to get every state in mdp and add it to self.values with value 0 
        # for i in range(self.iterations) 
        state_values = util.Counter() 
        # iterate for number of iterations 
        for i in range(self.iterations): 
            # for each state, we need to get the max action value
            for state in self.mdp.getStates(): 
                # Check for terminal state
                if self.mdp.isTerminal(state):
                    continue

                action_values = util.Counter()
                for action in self.mdp.getPossibleActions(state): 
                    action_values[action] = self.computeQValueFromValues(state, action)
                state_values[state] = action_values[action_values.argMax()]
            # get values after all of the iterations have been complete 
            for state in self.mdp.getStates(): 
                self.values[state] = state_values[state]


        # self.computeActionFromValues((0, 1))
        # util.raiseNotDefined()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q = 0 
        transition_states = self.mdp.getTransitionStatesAndProbs(state, action)
        for new_state, prob in transition_states: 
            q += prob * (self.mdp.getReward(state, action, new_state) + self.discount * self.values[new_state])

        return q

       # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        #  mdp.getStates()
        #       mdp.getPossibleActions(state)
        #       mdp.getTransitionStatesAndProbs(state, action)
        #       mdp.getReward(state, action, nextState)
        #       mdp.isTerminal(state)

        available_actions = self.mdp.getPossibleActions(state)
        # print(self.mdp.getTransitionStatesAndProbs(state, available_actions[0]))

        action_utility = None, -99999
        

        for current_action in available_actions: 
            current_utility = 0
            transition_states = self.mdp.getTransitionStatesAndProbs(state, current_action)

            for new_state, prob in transition_states: 
                current_utility += prob * (self.mdp.getReward(state, current_action, new_state) + self.discount * self.values[new_state])

            # check if current_utility is the greatest seen so far
            if current_utility > action_utility[1]: 
                action_utility = current_action, current_utility

        return action_utility[0]
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):

        state_values = util.Counter() 
        states = self.mdp.getStates()
        for i in range(self.iterations): 
            
            # use mod to have the current_state wrap around 
            current_state = states[i % len(states)]

            # go to next iteration of while loop if at a terminal state
            if self.mdp.isTerminal(current_state): 
                continue
            
            action_values = util.Counter()
            for action in self.mdp.getPossibleActions(current_state): 
                action_values[action] = self.computeQValueFromValues(current_state, action)
            state_values[current_state] = action_values[action_values.argMax()]
           
            for state in self.mdp.getStates(): 
                self.values[state] = state_values[state]




class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

