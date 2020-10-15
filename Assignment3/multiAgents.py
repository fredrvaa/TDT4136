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
import random, util, math

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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

    def maxValue(self, gameState, depth):
        """
        Finds max value of a perticular gamestate

        Args:
            gameState: state of the game to be assessed
            depth: depth of the game state
        Return:
            value: value of the game state

        This function is only used to calculate the value of pacman's actions,
        as he is the agent that tries to maximize the score.
        """

        # Check to see if game state is terminal
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Initialize value
        value = -math.inf
        
        # Iterate through the pacman agent's actions to find max value
        for action in gameState.getLegalActions():
            successorState = gameState.generateSuccessor(0, action)
            value = max(value, self.minValue(successorState, depth, 1))

        return value

    def minValue(self, gameState, depth, agentIndex):
        """
        Finds min value of a particular gamestate

        Args:
            gameState: state of the game to be assessed
            depth: depth of the game state
            agentIndex: index of ghost agent
        Return:
            value: value of the game state

        This function is only used to calculate the value of the ghost's actions, as
        these are the agents that tries to minimize the score.
        """

        # Check to see if game state is terminal
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Initialize value
        value = math.inf

        # Iterate through the ghost agent's actions to find the min value
        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex + 1 == gameState.getNumAgents():
                value = min(value, self.maxValue(successorState, depth - 1))
            else:
                value = min(value, self.minValue(successorState, depth, agentIndex + 1))

        return value

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

        bestAction = None
        bestValue = -math.inf

        # Iterate through the pacman agent's actions given the current gamestate.
        # This initializes an adversarial minimax search of depth=self.depth
        # Here, a depth of 1 means that all agents performs a move; first pacman
        # takes an action that maximizes the value, then each ghost takes an action that 
        # minimizes the value.
        for action in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0, action)
            value = self.minValue(successorState, self.depth, 1)
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxValue(self, gameState, depth, alpha, beta):
        """
        Finds max value of a perticular gamestate

        Args:
            gameState: state of the game to be assessed
            depth: depth of the game state
            alpha: maximizing players best value on path to root state
            beta: minimizing players best value on path to root state
        Return:
            value: value of the game state

        This function is only used to caluclate the value of pacman's actions,
        as he is the agent that tries to maximize the score.
        """

        # Check to see if game state is terminal
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Initialize value
        value = -math.inf
        
        # Iterate through the pacman agent's actions to find the max value
        # Remaining actions are pruned if an action is found such that this gameState
        # guarantees a higher value than a branch already visited by the minimizing agent.
        for action in gameState.getLegalActions():
            successorState = gameState.generateSuccessor(0, action)
            value = max(value, self.minValue(successorState, depth, 1, alpha, beta))
            if value > beta: return value
            alpha = max(alpha, value)

        return value

    def minValue(self, gameState, depth, agentIndex, alpha, beta):
        # Check to see if game state is terminal
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Initialize value
        value = math.inf

        # Iterate through the pacman agent's actions to find the max value
        # Remaining actions are pruned if an action is found such that this gameState
        # guarantees a lower value than a branch already visited by the maximizing agent.
        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex + 1 == gameState.getNumAgents():
                value = min(value, self.maxValue(successorState, depth - 1, alpha, beta))
            else:
                value = min(value, self.minValue(successorState, depth, agentIndex + 1, alpha, beta))

            if value < alpha: return value
            beta = min(beta, value)

        return value

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        bestAction = None
        bestValue = -math.inf
        alpha = -math.inf
        beta = math.inf


        # Iterate through the pacman agent's actions given the current gamestate.
        # This initializes an adversarial minimax search, with alpha-beta-pruning, of depth=self.depth
        # Here, a depth of 1 means that all agents performs a move; first pacman
        # takes an action that maximizes the value, then each ghost takes an action that 
        # minimizes the value. If values are found such that checking the remaining actions is redundant,
        # the reamining actions are pruned.
        for action in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0, action)
            value = self.minValue(successorState, self.depth, 1, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, value)

        return bestAction

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
