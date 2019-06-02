# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purstatees provided that (1) you do not distribute or publish
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
        The sequence must be comstateed of legal moves.
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    curr = problem.getStartState()
    actions = []
    path = [curr]
    while not problem.isGoalState(curr):
        successors = problem.getSuccessors(curr) # expand
        # check if current node can expand
        if len(successors) > 0:
            '''
            # randomize successor list
            util.FixedRandom().random.shuffle(successors)
            '''
            # find a successor not in path
            for state, act, cos in successors:
                if state not in path:
                    stack.push((path + [state], actions + [act]))
        path, actions = stack.pop()
        curr = path[-1]
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    curr = problem.getStartState()
    actions = []
    path = [curr]
    exp = []
    while not problem.isGoalState(curr):
        if curr in exp:
            successors = []
        else:
            successors = problem.getSuccessors(curr) # expand
            exp.append(curr)
        # check if current node can expand
        if len(successors) > 0:
            for state, act, _ in successors:
                if state not in path:
                    queue.push((path + [state], actions + [act]))
        if queue.isEmpty():
            break
        path, actions = queue.pop()
        curr = path[-1]
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    p_queue = util.PriorityQueue()
    curr = problem.getStartState()
    actions = []
    path = [curr]
    exp = []
    while not problem.isGoalState(curr):
        if curr in exp:
            successors = []
        else:
            successors = problem.getSuccessors(curr) # expand
            exp.append(curr)
        # check if current node can expand
        if len(successors) > 0:
            for state, act, _ in successors:
                if state not in path:
                    new_actions = actions + [act]
                    p_queue.push((path + [state], new_actions), problem.getCostOfActions(new_actions))
        if p_queue.isEmpty():
            break
        path, actions = p_queue.pop()
        curr = path[-1]
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # "*** YOUR CODE HERE ***"
    p_queue = util.PriorityQueue()
    curr = problem.getStartState()
    actions = []
    path = [curr]
    exp = []
    while not problem.isGoalState(curr):
        if curr in exp:
            successors = []
        else:
            successors = problem.getSuccessors(curr) # expand
            exp.append(curr)
        # check if current node can expand
        if len(successors) > 0:
            for state, act, _ in successors:
                if state not in path:
                    new_actions = actions + [act]
                    new_cost = problem.getCostOfActions(new_actions) + heuristic(state, problem)
                    p_queue.push((path + [state], new_actions), new_cost)
        if p_queue.isEmpty():
            break
        path, actions = p_queue.pop()
        curr = path[-1]
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
