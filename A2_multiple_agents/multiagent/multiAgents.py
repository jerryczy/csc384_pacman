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
    # prev_move = 'Stop'

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        newPos = successorGameState.getPacmanPosition() # tuple
        newFood = successorGameState.getFood() # grid
        oldFood = currentGameState.getFood()
        capsules = currentGameState.getCapsules()
        newGhostStates = successorGameState.getGhostStates() # list
        GhostPos = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # list

        "*** YOUR CODE HERE ***"
        score = -9999999
        if action == 'Stop': return score
        for idx, ghost in enumerate(GhostPos):
            if ghost == newPos and newScaredTimes[idx] == 0:
                return score
        if not newFood.asList():
            return score * (-1)
        if newPos in oldFood.asList():
            return 1
        if newPos in capsules:
            return 1
        for food in newFood.asList():
            dis = (-1) * manhattanDistance(food, newPos)
            if dis > score:
                score = dis

        return score

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
        """
        "*** YOUR CODE HERE ***"
        decision_tree = {}
        game_states = [(gameState, None)]
        num_agent = gameState.getNumAgents()
        layer = 0
        terminate = gameState.isWin() or gameState.isLose()

        while layer//num_agent < self.depth and not terminate:
            next_layer = []
            index = layer % num_agent
            for state, _ in game_states:
                legal_actions = state.getLegalActions(index)
                new_states = [(state.generateSuccessor(index, action), action) for action in legal_actions]
                if new_states:
                    decision_tree[state] = new_states
                next_layer.extend(new_states)
            game_states = next_layer
            layer += 1

        # empty tree
        if not decision_tree:
            return None

        scores = [self.evaluate(1, decision_tree, state, num_agent) for state, action in decision_tree[gameState]]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return decision_tree[gameState][chosenIndex][1]

    def evaluate(self, counter, tree, curr_state, num_agent):
        if curr_state.isWin():
            return 999999
        elif curr_state.isLose():
            return -99999
        if curr_state not in tree:
            return 0
        scores = []
        for state, _ in tree[curr_state]:
            if state in tree:
                scores.append(self.evaluate(counter+1, tree, state, num_agent))
            else:
                scores.append(self.evaluationFunction(state))
        if counter % num_agent == 0:
            bestScore = max(scores)
        else:
            bestScore = min(scores)
        return bestScore

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        if self.depth == 0: # only look at current state
            return self.evaluationFunction(gameState)

        num_agent = gameState.getNumAgents()
        # (alpha, beta, value, parent, action, children, layer)
        decision_tree = {gameState: [float('-inf'), float('inf'), None, None, None, [], 0]}
        value, action = self.generate_value(num_agent, decision_tree, gameState)
        return action

    def generate_value(self, num_agent, tree, state):
        alpha, beta, value, parent, action, children, layer = tree[state]
        if parent:
            alpha, beta, _, _, _, _, _ = tree[parent]
            tree[state] = [alpha, beta, value, parent, action, children, layer]
        index = layer % num_agent
        legal_actions = state.getLegalActions(index)
        values = []
        actions = []
        successors = []
        for act in legal_actions:
            successor = state.generateSuccessor(index, act)
            successors.append(successor)
            tree[successor] = [alpha, beta, None, state, act, [], layer + 1]
            if (layer+1)//num_agent == self.depth or successor.isWin() or successor.isLose():
                # depth reach or terminal node reached
                value = self.evaluationFunction(successor)
            else:
                if not children: # no children, need expand to next level
                    value, action = self.generate_value(num_agent, tree, successor)
            
            if index == 0 and value > alpha: # state max
                tree[state][0] = value
                tree[state][2] = value
                alpha = value
            elif index > 0 and value < beta: # min
                tree[state][1] = value
                tree[state][2] = value
                beta = value
            actions.append(act)
            values.append(value)
            if alpha >= beta: break
        tree[state][5] = successors
        if index == 0: # max
            best_value =  max(values)
        else:
            best_value =  min(values)
        indicies = [index for index in range(len(values)) if values[index] == best_value]
        return (best_value, actions[indicies[0]])

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
        decision_tree = {}
        game_states = [(gameState, None)]
        num_agent = gameState.getNumAgents()
        layer = 0
        terminate = gameState.isWin() or gameState.isLose()

        while layer//num_agent < self.depth and not terminate:
            next_layer = []
            for state, _ in game_states:
                index = layer % num_agent
                legal_actions = state.getLegalActions(index)
                new_states = [(state.generateSuccessor(index, action), action) for action in legal_actions]
                if new_states:
                    decision_tree[state] = new_states
                next_layer.extend(new_states)
            game_states = next_layer
            layer += 1

        # empty tree
        if not decision_tree:
            return None

        scores = [self.evaluate(1, decision_tree, state, num_agent) for state, action in decision_tree[gameState]]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        
        return decision_tree[gameState][chosenIndex][1]

    def evaluate(self, counter, tree, curr_state, num_agent):
        if curr_state.isWin():
            return 999999
        elif curr_state.isLose():
            return -99999
        if curr_state not in tree:
            return 0
        scores = []
        for state, _ in tree[curr_state]:
            if state in tree:
                scores.append(self.evaluate(counter+1, tree, state, num_agent))
            else:
                scores.append(self.evaluationFunction(state))
        if counter % num_agent == 0:
            bestScore = max(scores)
        else:
            bestScore = float(sum(scores)) / max(len(scores), 1)
        return bestScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()

    for ghost in ghostStates:
        if ghost.getPosition() == pos and ghost.scaredTimer == 0:
            return -999999

    if currentGameState.isLose():
        return -999999
    if currentGameState.isWin():
        return 999999
    if currentGameState.getNumFood() == 0:
        return 999999
    if not food_list:
        return 999999

    score = 10 * currentGameState.getScore()

    food_score = 0
    for food in food_list:
        food_score += manhattanDistance(food, pos)
    score -= food_score ** 0.7
    score -= len(food_list)
    for cap in capsules:
        score -= len(capsules) * manhattanDistance(cap, pos)
    return score
    

# Abbreviation
better = betterEvaluationFunction

