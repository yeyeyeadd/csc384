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
        scores = [self.evaluationFunction(gameState, action) for action in
                  legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if
                       scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in
                          newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        for foodPos in newFood.asList():
            distance = manhattanDistance(foodPos, newPos)
            if distance != 0:
                score += 1.0 / distance
        for ghostState in newGhostStates:
            distance = manhattanDistance(ghostState.getPosition(), newPos)
            if distance != 0 and ghostState.scaredTimer == 0:
                score -= 1.0 / distance

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        return self.DPMinMax(gameState, 0, 0)

    def DPMinMax(self, gameState, agent, depth):
        best_move = None

        if gameState.isLose() or gameState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agent)

        value = float('-inf') if agent == 0 else float('inf')

        if agent == gameState.getNumAgents() - 1:
            nxt_agent = 0
        else:
            nxt_agent = agent + 1
        for action in actions:
            nxt_state = gameState.generateSuccessor(agent, action)
            if agent == 0:
                nxt_value = self.DPMinMax(nxt_state, nxt_agent, depth)
                if nxt_value > value:
                    value = nxt_value
                    best_move = action

            else:
                nxt_depth = depth + 1 if nxt_agent == 0 else depth
                nxt_value = self.DPMinMax(nxt_state, nxt_agent, nxt_depth)
                value = min(nxt_value, value)
        if depth == 0 and agent == 0:
            return best_move
        else:
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
        return self.AplhaBeta(gameState, 0, float('-inf'), float('inf'), 0)

    def AplhaBeta(self, gameState, agent, alpha, beta, depth):
        best_move = None

        if gameState.isLose() or gameState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agent)

        value = float('-inf') if agent == 0 else float('inf')

        if agent == gameState.getNumAgents() - 1:
            nxt_agent = 0
        else:
            nxt_agent = agent + 1
        for action in actions:
            nxt_state = gameState.generateSuccessor(agent, action)
            if agent == 0:
                nxt_value = self.AplhaBeta(nxt_state, nxt_agent, alpha, beta,
                                           depth)
                if value < nxt_value:
                    value = nxt_value
                    best_move = action
                if value >= beta:
                    break
                alpha = max(alpha, value)
            else:
                nxt_depth = depth + 1 if nxt_agent == 0 else depth
                nxt_value = self.AplhaBeta(nxt_state, nxt_agent, alpha, beta,
                                           nxt_depth)
                value = min(nxt_value, value)
                if value <= alpha:
                    break
                beta = min(beta, value)
        if depth == 0 and agent == 0:
            return best_move
        else:
            return value


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

        return self.Expectimax(gameState, 0, 0)

    def Expectimax(self, gameState, agent, depth):
        best_move = None

        if gameState.isLose() or gameState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agent)

        if agent == 0:
            value = float("-inf")
        else:
            value = 0

        if agent == gameState.getNumAgents() - 1:
            nxt_agent = 0
        else:
            nxt_agent = agent + 1

        for action in actions:
            nxt_state = gameState.generateSuccessor(agent, action)
            if agent == 0:
                nxt_value = self.Expectimax(nxt_state, nxt_agent, depth)
                if value < nxt_value:
                    value = nxt_value
                    best_move = action
            else:
                nxt_depth = depth + 1 if nxt_agent == 0 else depth
                nxt_value = self.Expectimax(nxt_state, nxt_agent, nxt_depth)
                value += nxt_value
        if depth == 0 and agent == 0:
            return best_move
        elif agent == 0:
            return value
        else:
            return float(value) / float(len(actions))


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <1.Firsts we sum all the distance(by bfs) between foods and pacman, and times a 4/distance
    2.Next we consider the ghosts distance(by bfs), if pacman can eat it, we should go eat it, otherwise we should run away from it.
    3.we should eat capsule if we pass by(then we can go eat ghost to get more points)>
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    ghost_state = currentGameState.getGhostStates()
    ghostScaredTimes = [ghostState.scaredTimer for ghostState in ghost_state]
    score = currentGameState.getScore()

    # for ghost_state in ghost_state:
    #     ghost_pos = ghost_state.getPosition()
    #     distance = manhattanDistance(position, ghost_pos)
    #     if ghost_state.scaredTimer >= 1 and distance != 0:
    #         score += (1.0 / distance) * 100
    #     elif distance != 0 and distance <= 4:
    #         score -= 1.0 / distance * 100

    distance_ghost, distance_food = BFS_distance(currentGameState)
    for i in distance_food:
        if i != 0:
            score += 4.0 / i
    for i in range(len(distance_ghost)):
        if ghostScaredTimes[i] >= 1 and distance_ghost[i] != 0:
            score += 1.0 / distance_ghost[i] * 100
        elif distance_ghost[i] != 0 and distance_ghost[i] <= 5 and ghostScaredTimes[i] == 0:
            score -= 1.0 / distance_ghost[i] * 100

    # for food in foods.asList():
    #     distance = manhattanDistance(position, food)
    #     if distance != 0:
    #         score += 1.0 / distance * 4
    score += sum(ghostScaredTimes)
    score -= len(currentGameState.getCapsules()) * 2

    return score


def BFS_distance(currentGameState):
    position = currentGameState.getPacmanPosition()
    x = position[0]
    y = position[1]
    distance_food = []
    ghost_pos = []
    ghosts_state = currentGameState.getGhostStates()
    for ghost in ghosts_state:
        ghost_pos.append(ghost.getPosition())
    ghost_left = len(ghost_pos)
    ghost_add = []
    distance_ghost= []

    walls = currentGameState.getWalls()
    walls_copy = walls.copy()
    walls_copy[x][y] = "p"
    food = currentGameState.getFood()
    food_pos = food.asList()
    food_left = len(food_pos)
    food_add = []
    q = [(x, y, 0)]

    while q and food_left:
        x, y, s = q.pop(0)
        for x_next, y_next in [(x + 1, y), (x, y + 1), (x, y - 1),
                               (x - 1, y)]:

            if (x_next, y_next) in ghost_pos and (x_next, y_next) not in ghost_add:
                distance_ghost.append(s + 1)
                ghost_add.append((x_next, y_next))
                ghost_left -= 1

            if food[x_next][y_next] and (x_next, y_next) not in food_add:
                distance_food.append(s + 1)
                food_add.append((x_next, y_next))
                food_left -= 1

            if 0 <= x_next < walls_copy.width and 0 <= y_next < walls_copy.height:
                if not walls_copy[x_next][y_next]:
                    walls_copy[x_next][y_next] = s + 1
                    q.append((x_next, y_next, s + 1))

    return distance_ghost, distance_food


def BFS_distance_ghost(currentGameState):
    position = currentGameState.getPacmanPosition()
    x = position[0]
    y = position[1]
    distance = []

    walls = currentGameState.getWalls()
    walls_copy = walls.copy()
    walls_copy[x][y] = "p"
    ghost_pos = []
    ghosts_state = currentGameState.getGhostStates()
    for ghost in ghosts_state:
        ghost_pos.append(ghost.getPosition())
    ghost_left = len(ghost_pos)
    ghost_add = []
    q = [(x, y, 0)]

    while q and ghost_left:
        x, y, s = q.pop(0)
        for x_next, y_next in [(x + 1, y), (x, y + 1), (x, y - 1),
                               (x - 1, y)]:
            if (x_next, y_next) in ghost_pos and (x_next, y_next) not in ghost_add:
                distance.append(s + 1)
                ghost_add.append((x_next, y_next))
                ghost_left -= 1

            if 0 <= x_next < walls_copy.width and 0 <= y_next < walls_copy.height:
                if not walls_copy[x_next][y_next]:
                    walls_copy[x_next][y_next] = s + 1
                    q.append((x_next, y_next, s + 1))
    return distance

# Abbreviation
better = betterEvaluationFunction
