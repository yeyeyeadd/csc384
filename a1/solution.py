
#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files
import math
import itertools
import os  # for time functions

from numpy.ma import empty

from search import *  # for search engines
from sokoban import SokobanState, Direction, \
    PROBLEMS  # for Sokoban specific classes and problems


def sokoban_goal_state(state):
    '''
  @return: Whether all boxes are stored.
  '''
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    total = 0
    for box in state.boxes:
        minimum = -1
        for storage in state.storage:
            distance = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
            if (minimum == -1) or (minimum >= distance):
                minimum = distance
        total += minimum
    return total


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    if is_dead_bot(state):
        return math.inf
    total = manhattan_dis(state)
    total += obstacles_dis(state)
    total += box_dis(state)
    return total


def is_dead_bot(state):
    conner = [(0, 0), (state.width - 1, state.height - 1),
              (0, state.height - 1), (state.width - 1, 0)]
    for box in state.boxes:
        if box not in state.storage:
            if box in conner:
                return True
            elif box[0] == 0 and ((0, box[1] + 1) in state.obstacles or (
                    0, box[1] - 1) in state.obstacles):
                return True
            elif box[0] == 0 and ((0, box[1] + 1) in state.boxes or (
                    0, box[1] - 1) in state.boxes):
                return True
            elif box[0] == state.width - 1 and (
                    (state.width - 1, box[1] + 1) in state.obstacles or (
                    state.width - 1, box[1] - 1) in state.obstacles):
                return True
            elif box[0] == state.width - 1 and (
                    (state.width - 1, box[1] + 1) in state.boxes or (
                    state.width - 1, box[1] - 1) in state.boxes):
                return True
            elif box[1] == 0 and ((box[0] + 1, 0) in state.obstacles or (
                    box[0] - 1, 0) in state.obstacles):
                return True
            elif box[1] == state.height - 1 and (
                    (box[0] + 1, state.height - 1) in state.obstacles or (
                    box[0] - 1, state.height - 1) in state.obstacles):
                return True
            elif box[1] == 0 and ((box[0] + 1, 0) in state.boxes or (
                    box[0] - 1, 0) in state.boxes):
                return True
            elif box[1] == state.height - 1 and (
                    (box[0] + 1, state.height - 1) in state.boxes or (
                    box[0] - 1, state.height - 1) in state.boxes):
                return True
            elif ((box[0] - 1, box[1]) in state.obstacles) and (
                    ((box[0], box[1] + 1) in state.obstacles) or (
                    (box[0], box[1] - 1) in state.obstacles)):
                return True
            elif ((box[0] + 1, box[1]) in state.obstacles) and (
                    ((box[0], box[1] + 1) in state.obstacles) or (
                    (box[0], box[1] - 1) in state.obstacles)):
                return True
            elif ((box[0] + 1, box[1]) in state.boxes) and (((box[0] + 1, box[
                                                                              1] + 1) in state.obstacles and (
                                                                     box[0],
                                                                     box[
                                                                         1] + 1) in state.obstacles) or (
                                                                    (box[0] + 1,
                                                                     box[
                                                                         1] - 1) in state.obstacles and (
                                                                            box[
                                                                                0],
                                                                            box[
                                                                                1] - 1) in state.obstacles)):
                return True
            elif ((box[0] - 1, box[1]) in state.boxes) and (((box[0] - 1, box[
                                                                              1] + 1) in state.obstacles and (
                                                                     box[0],
                                                                     box[
                                                                         1] + 1) in state.obstacles) or (
                                                                    (box[0] - 1,
                                                                     box[
                                                                         1] - 1) in state.obstacles and (
                                                                            box[
                                                                                0],
                                                                            box[
                                                                                1] - 1) in state.obstacles)):
                return True
            elif ((box[0], box[1] + 1) in state.boxes) and (((box[0] + 1, box[
                                                                              1] + 1) in state.obstacles and (
                                                                     box[0] + 1,
                                                                     box[
                                                                         1]) in state.obstacles) or (
                                                                    (box[0] - 1,
                                                                     box[
                                                                         1] + 1) in state.obstacles and (
                                                                            box[
                                                                                0] - 1,
                                                                            box[
                                                                                1]) in state.obstacles)):
                return True
            elif ((box[0], box[1] - 1) in state.boxes) and (((box[0] + 1, box[
                                                                              1] - 1) in state.obstacles and (
                                                                     box[0] + 1,
                                                                     box[
                                                                         1]) in state.obstacles) or (
                                                                    (box[0] - 1,
                                                                     box[
                                                                         1] + 1) in state.obstacles and (
                                                                            box[
                                                                                0] - 1,
                                                                            box[
                                                                                1]) in state.obstacles)):
                return True
    return False


def manhattan_dis(state):
    total_lst = []
    for box in state.boxes:
        dis = []
        if box[0] == 0:
            for storage in state.storage:
                if storage[0] == 0:
                    curr_dis = abs(storage[0] - box[0]) + abs(
                        storage[1] - box[1])
                else:
                    curr_dis = math.inf
                dis.append(curr_dis)
        elif box[0] == state.width - 1:
            for storage in state.storage:
                if storage[0] == state.width - 1:
                    curr_dis = abs(storage[0] - box[0]) + abs(
                        storage[1] - box[1])
                else:
                    curr_dis = math.inf
                dis.append(curr_dis)
        elif box[1] == 0:
            for storage in state.storage:
                if storage[1] == 0:
                    curr_dis = abs(storage[0] - box[0]) + abs(
                        storage[1] - box[1])
                else:
                    curr_dis = math.inf
                dis.append(curr_dis)
        elif box[1] == state.height - 1:
            for storage in state.storage:
                if storage[1] == state.height - 1:
                    curr_dis = abs(storage[0] - box[0]) + abs(
                        storage[1] - box[1])
                else:
                    curr_dis = math.inf
                dis.append(curr_dis)
        else:
            for storage in state.storage:
                curr_dis = abs(storage[0] - box[0]) + abs(
                    storage[1] - box[1])
                dis.append(curr_dis)
        if min(dis) == math.inf:
            return math.inf
        total_lst.append(dis)

    n_box = len(state.boxes)
    n_storage = len(state.storage)
    all_comb = list(itertools.combinations(list(range(0, n_storage)),
                                           n_box))
    total = math.inf
    all_pair = []
    for comb in all_comb:
        pair = list(itertools.permutations(comb))
        all_pair.extend(pair)
    for pair in all_pair:
        summation = 0
        for i in range(0, n_box):
            summation += total_lst[i][pair[i]]
        if summation < total:
            total = summation
    return total


def obstacles_dis(state):
    nearest_storage = []
    for box in state.boxes:
        storage_copy = list(state.storage)
        min_dis = math.inf
        min_storage = None
        i = 0
        while len(storage_copy) != 0:
            curr = storage_copy[0]
            dis = abs(curr[0] - box[0]) + abs(curr[1] - box[1])
            if dis < min_dis:
                min_dis = dis
                min_storage = storage_copy[i]
            del storage_copy[0]
        nearest_storage.append(min_storage)
    num_box = len(state.boxes)
    acc = 0
    for i in range(0, num_box):
        boxes = list(state.boxes)
        curr_box = boxes[i]
        curr_storage = nearest_storage[i]
        if not curr_box == curr_storage:
            low_x = min(curr_box[0], curr_storage[0])
            low_y = min(curr_box[1], curr_storage[1])
            high_x = max(curr_box[0], curr_storage[0])
            high_y = max(curr_box[1], curr_storage[1])
            for x in range(low_x + 1, high_x):
                if (x, low_y) in state.obstacles:
                    acc += 1
                if (x, high_y) in state.obstacles:
                    acc += 1
            for y in range(low_y + 1, high_y):
                if (low_x, y) in state.obstacles:
                    acc += 1
                if (high_x, y) in state.obstacles:
                    acc += 1
    return acc * 8


def box_dis(state):
    acc = 0
    for box in state.boxes:
        if box not in state.storage:
            x = box[0]
            y = box[1]
            near = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
            for i in near:
                if i in state.boxes:
                    acc += 1
    return 2 * acc


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the standard form of weighted A* (i.e. g + w*h)

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime weighted astar algorithm'''
    start_time = os.times()[0]
    se = SearchEngine('custom', 'default')
    se.init_search(initial_state, sokoban_goal_state, heur_fn,
                   (lambda sN: fval_function(sN, weight)))
    got_it = False
    curr_cost = math.inf

    while (os.times()[0] < start_time + timebound) and (not se.open.empty()):
        time_left = timebound - (- start_time + os.times()[0])
        goal = se.search(time_left, [math.inf, math.inf, curr_cost])[0]
        if not goal:
            return got_it
        elif curr_cost > goal.gval + heur_fn(goal):
            got_it = goal
            curr_cost = goal.gval + heur_fn(goal)
            if weight >= 2:
                weight -= 1
    return got_it


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime greedy best-first search'''
    start_time = os.times()[0]
    se = SearchEngine('best_first', 'default')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)
    got_it = False
    curr_cost = math.inf

    while (os.times()[0] < start_time + timebound) and (not se.open.empty()):
        time_left = timebound - (- start_time + os.times()[0])
        goal = se.search(time_left, [curr_cost, math.inf, math.inf])[0]
        if not goal:
            return got_it
        elif curr_cost > goal.gval:
            got_it = goal
            curr_cost = goal.gval
    return got_it
