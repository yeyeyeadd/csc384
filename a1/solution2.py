#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files
import math
import csv
import itertools
import os  # for time functions
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
    sum = 0
    for box in state.boxes:
        minimum = -1
        for storage_point in state.storage:
            dis = abs(storage_point[0] - box[0]) + abs(
                storage_point[1] - box[1])
            if (minimum == -1) or (dis < minimum):
                minimum = dis
        sum += minimum
    return sum


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
    '''a better heuristic
    The distance is now calculated based on unique pair betweem box and storage, and the sum of distance should
    be the minimum sum. Box block or obstacle on the path from box to goal storage increase hval.
    '''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    result = unique_manhattan(state)
    # result += corner_gravity(state)
    result += box_block(state)
    result += obs(state)
    return result


def unique_manhattan(state):
    temp = []
    for box in state.boxes:
        tp = []
        if box[0] == 0:
            # flag = 'Left'
            for storage_point in state.storage:
                if storage_point[0] == 0:
                    dis = abs(storage_point[0] - box[0]) + abs(
                        storage_point[1] - box[1])
                else:
                    dis = math.inf
                tp.append(dis)
        elif box[0] == state.width - 1:
            # flag = 'Right'
            for storage_point in state.storage:
                if storage_point[0] == state.width - 1:
                    dis = abs(storage_point[0] - box[0]) + abs(
                        storage_point[1] - box[1])
                else:
                    dis = math.inf
                tp.append(dis)
        elif box[1] == 0:
            # flag = 'Bottom'
            for storage_point in state.storage:
                if storage_point[1] == 0:
                    dis = abs(storage_point[0] - box[0]) + abs(
                        storage_point[1] - box[1])
                else:
                    dis = math.inf
                tp.append(dis)
        elif box[1] == state.height - 1:
            # flag = 'Top'
            for storage_point in state.storage:
                if storage_point[0] == state.height - 1:
                    dis = abs(storage_point[0] - box[0]) + abs(
                        storage_point[1] - box[1])
                else:
                    dis = math.inf
                tp.append(dis)
        else:
            # flag = 'Middle'
            for storage_point in state.storage:
                dis = abs(storage_point[0] - box[0]) + abs(
                    storage_point[1] - box[1])
                tp.append(dis)
        if min(tp) == math.inf:
            return math.inf
        temp.append(tp)

    num_box = len(state.boxes)
    num_storage = len(state.storage)
    combs = list(itertools.combinations(list(range(0, num_storage)), num_box))
    pers = []
    for comb in combs:
        sub_pers = list(itertools.permutations(comb))
        pers.extend(sub_pers)
    mini = math.inf
    for per in pers:
        sum = 0
        for i in range(0, num_box):
            sum += temp[i][per[i]]
        if sum < mini:
            mini = sum
    return mini


def box_block(state):
    num = 0
    for box in state.boxes:
        if box not in state.storage:
            x = box[0]
            y = box[1]
            adj_lst = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
            for adj in adj_lst:
                if adj in state.boxes:
                    num += 1
    return 2 * num


def corner_gravity(state):
    corners = detect_corner(state)
    if corners == []:
        return 0
    corner = corners.pop()
    min_dis = math.inf
    for box in state.boxes:
        dis = abs(corner[0] - box[0]) + abs(corner[1] - box[1])
        if dis < min_dis:
            min_dis = dis
    return min_dis * 1


def detect_corner(state):
    w = state.width
    h = state.height
    corners = [(0, 0), (0, h - 1), (w - 1, 0), (w - 1, h - 1)]
    behave_corners = []
    for corner in corners:
        if corner in state.storage:
            behave_corners.append(corner)
    real_corners = []
    for corner in behave_corners:
        mid = (w / 2, h / 2)
        x_dir = (mid[0] - corner[0]) / abs(mid[0] - corner[0])
        y_dir = (mid[1] - corner[1]) / abs(mid[1] - corner[1])
        if corner not in state.boxes:
            real_corners.append(corner)
        else:
            temp_corner_x = (corner[0] + x_dir, corner[1])
            temp_corner_y = (corner[0], corner[1] + y_dir)
            flag = True
            while temp_corner_x in state.storage and flag == True:
                if temp_corner_x not in state.boxes:
                    real_corners.append(temp_corner_x)
                    flag = False
                else:
                    temp_corner_x = (temp_corner_x[0] + x_dir, temp_corner_x[1])

            flag = True
            while temp_corner_y in state.storage and flag == True:
                if temp_corner_y not in state.boxes:
                    real_corners.append(temp_corner_y)
                    flag = False
                else:
                    temp_corner_y = (temp_corner_y[0], temp_corner_y[1] + y_dir)
    return real_corners


def obs(state):
    nearest_storage = []
    for box in state.boxes:
        min_dis = math.inf
        min_storage = None
        for storage in state.storage:
            dis = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
            if dis < min_dis:
                min_dis = dis
                min_storage = storage
        nearest_storage.append(min_storage)
    num_box = len(state.boxes)
    num_obs = 0
    for i in range(0, num_box):
        boxes = list(state.boxes)
        curr_box = boxes[i]
        curr_storage = nearest_storage[i]
        position = pos(curr_box, curr_storage)
        if position == 'same_pos':
            num_obs += 0
        else:
            low_x = min(curr_box[0], curr_storage[0])
            low_y = min(curr_box[1], curr_storage[1])
            high_x = max(curr_box[0], curr_storage[0])
            high_y = max(curr_box[1], curr_storage[1])
            for x in range(low_x + 1, high_x):
                if (x, low_y) in state.obstacles:
                    num_obs += 1
                if (x, high_y) in state.obstacles:
                    num_obs += 1
            for y in range(low_y + 1, high_y):
                if (low_x, y) in state.obstacles:
                    num_obs += 1
                if (high_x, y) in state.obstacles:
                    num_obs += 1
    return num_obs * 8


def pos(a, b):
    if a == b:
        return 'same_pos'
    elif a[0] == b[0]:
        return 'same_column'
    elif a[1] == b[1]:
        return 'same_row'
    else:
        return 'diff_pos'


def dead_state(state):
    pass


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


def fval_function_XUP(sN, weight):
    # IMPLEMENT
    """
    Another custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the XUP form of weighted A*

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    return (1 / (2 * weight)) * \
           (sN.gval + sN.hval + math.sqrt(
               (sN.gval + sN.hval) ** 2 + 4 * weight * (weight - 1) * (
                       sN.hval ** 2)))


def fval_function_XDP(sN, weight):
    # IMPLEMENT
    """
    A third custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the XDP form of weighted A*

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    return (1 / (2 * weight)) * \
           (sN.gval + (2 * weight - 1) * sN.hval + math.sqrt(
               (sN.gval - sN.hval) ** 2 + 4 * weight * sN.gval * sN.hval))


def compare_weighted_astars():
    # IMPLEMENT
    '''Compares various different implementations of A* that use different f-value functions'''
    '''INPUT: None'''
    '''OUTPUT: None'''
    """
    This function should generate a CSV file (comparison.csv) that contains statistics from
    4 varieties of A* search on 3 practice problems.  The four varieties of A* are as follows:
    Standard A* (Variant #1), Weighted A*  (Variant #2),  Weighted A* XUP (Variant #3) and Weighted A* XDP  (Variant #4).  
    Format each line in your your output CSV file as follows:

    A,B,C,D,E,F

    where
    A is the number of the problem being solved (0,1 or 2)
    B is the A* variant being used (1,2,3 or 4)
    C is the weight being used (2,3,4 or 5)
    D is the number of paths extracted from the Frontier (or expanded) during the search
    E is the number of paths generated by the successor function during the search
    F is the overall solution cost    

    Note that you will submit your CSV file (comparison.csv) with your code
    """

    header = ['problem', 'A*_type', 'weight', 'p_ext', 'p_gen', 'cost']
    with open('comparison.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    for i in range(0, 3):
        problem = PROBLEMS[i]
        for weight in [2, 3, 4, 5]:
            # you can write code in here if you like
            # B == 2, 3, 4
            func_list = [fval_function, fval_function_XUP, fval_function_XDP]
            for j in range(0, 3):
                se = SearchEngine('custom', 'default')
                wrapped_fval_function = lambda sN: func_list[j](sN, weight)
                se.init_search(problem, sokoban_goal_state,
                               heur_manhattan_distance, wrapped_fval_function)
                goal, stats = se.search()
                if goal:
                    data = [i, j + 2, weight, stats.states_expanded,
                            stats.states_generated, goal.gval]
                else:
                    data = [i, j + 2, weight, 'FAIL', 'FAIL', 'FAIL']
                with open('comparison.csv', 'a', encoding='UTF8',
                          newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)
        se_A = SearchEngine('astar', 'default')
        se_A.init_search(problem, sokoban_goal_state, heur_manhattan_distance)
        goal, stats = se_A.search()
        if goal:
            data = [i, 1, 'N/A', stats.states_expanded, stats.states_generated,
                    goal.gval]
        else:
            data = [i, 1, 'N/A', 'FAIL', 'FAIL', 'FAIL']
        with open('comparison.csv', 'a', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    start_time = os.times()[0]
    se = SearchEngine('custom', 'default')
    wrapped_fval_function = lambda sN: fval_function_XDP(sN, weight)
    se.init_search(initial_state, sokoban_goal_state, heur_fn,
                   wrapped_fval_function)
    curr = False
    curr_cost = math.inf

    while (not se.open.empty()) and (os.times()[0] < start_time + timebound):
        time_left = timebound - (- start_time + os.times()[0])
        goal = se.search(time_left, [math.inf, math.inf, curr_cost])[0]
        if goal == False:
            return curr
        elif curr_cost > goal.gval + heur_fn(goal):
            curr = goal
            curr_cost = goal.gval + heur_fn(goal)
            if weight >= 2:
                weight += 1
    return curr


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of anytime greedy best-first search'''
    start_time = os.times()[0]
    se = SearchEngine('best_first', 'default')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)
    curr = False
    curr_cost = math.inf

    while (not se.open.empty()) and (os.times()[0] < start_time + timebound):
        time_left = timebound - (- start_time + os.times()[0])
        goal = se.search(time_left, [curr_cost, math.inf, math.inf])[0]
        if goal == False:
            return curr
        elif curr_cost > goal.gval:
            curr = goal
            curr_cost = goal.gval
    return curr
