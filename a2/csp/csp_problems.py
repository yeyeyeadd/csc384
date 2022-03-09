from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search


##################################################################
### NQUEENS
##################################################################

def nQueens(n, tableCnstr):
    '''Return an n-queens CSP, optionally use tableContraints'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i + 1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []
    for qi in range(len(dom)):
        for qj in range(qi + 1, len(dom)):
            if tableCnstr:
                con = QueensTableConstraint("C(Q{},Q{})".format(qi + 1, qj + 1),
                                            vars[qi], vars[qj], qi + 1, qj + 1)
            else:
                con = QueensConstraint("C(Q{},Q{})".format(qi + 1, qj + 1),
                                       vars[qi], vars[qj], qi + 1, qj + 1)
            cons.append(con)

    csp = CSP("{}-Queens".format(n), vars, cons)
    return csp


def solve_nQueens(n, algo, allsolns, tableCnstr=False,
                  variableHeuristic='fixed', trace=False):
    '''Create and solve an nQueens CSP problem. The first
       parameer is 'n' the number of queens in the problem,
       The second specifies the search algorithm to use (one
       of 'BT', 'FC', or 'GAC'), the third specifies if
       all solutions are to be found or just one, variableHeuristic
       specfies how the next variable is to be selected
       'random' at random, 'fixed' in a fixed order, 'mrv'
       minimum remaining values. Finally 'trace' if specified to be
       'True' will generate some output as the search progresses.
    '''
    csp = nQueens(n, tableCnstr)
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns,
                                     trace)
    print("Explored {} nodes".format(num_nodes))
    if len(solutions) == 0:
        print("No solutions to {} found".format(csp.name()))
    else:
        print("Solutions to {}:".format(csp.name()))
        i = 0
        for s in solutions:
            i += 1
            print("Solution #{}: ".format(i), )
            for (var, val) in s:
                print("{} = {}, ".format(var.name(), val), )
            print("")


##################################################################
### SUDOKU
##################################################################

def sudokuCSP(initial_sudoku_board, model='neq'):
    '''The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board

       -------------------
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists

       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]


       Construct and return CSP for solving this sudoku board using
       binary not equals if model='neq' or using allDiff constraints
       if model='alldiff'

       The CSP contains a variable for each cell of the board with
       with domain equal to {1-9} if the board has a 0 at that position,
       and domain equal {i} if the board has a fixed number i at that
       cell.

       The CSP has a neq constraint between every relevant pair of
       varibles, or an alldiff constraint between every set of
       variables in a row, column, or sub-square

    '''
    # your implementation for Question 4 changes this function
    # implement handling of model == 'alldiff'

    if not model in ['neq', 'alldiff']:
        print("Error wrong sudoku model specified {}. Must be one of {}".format(
            model, ['neq', 'alldiff']))

    # first define the variables
    i = 0
    var_array = []
    for row_list in initial_sudoku_board:
        var_array.append([])
        j = 0
        for col in row_list:
            cell = initial_sudoku_board[i][j]
            if cell == 0:
                dom = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                dom = [cell]
            var = Variable("V{},{}".format(i + 1, j + 1), dom)
            var_array[i].append(var)
            j += 1
        i += 1

    # Set up the constraints
    # row constraints
    constraint_list = []

    for row in var_array:
        if model == 'neq':
            constraint_list.extend(post_all_pairs(row))
        elif model == 'alldiff':
            name = "row" + str(var_array.index(row))
            constraint_list.append(AllDiffConstraint(name, row))
    for colj in range(len(var_array[0])):
        scope = list(map(lambda row: row[colj], var_array))
        if model == 'neq':
            constraint_list.extend(post_all_pairs(scope))
        elif model == 'alldiff':
            name = "row" + str(colj)
            constraint_list.append(AllDiffConstraint(name, scope))

    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            # initial upper left hand index of subsquare
            scope = []
            for k in [0, 1, 2]:
                for l in [0, 1, 2]:
                    scope.append(var_array[i + k][j + l])
            if model == 'neq':
                constraint_list.extend(post_all_pairs(scope))
            elif model == 'alldiff':
                name = "subsquare" + str(i) + " " + str(j)
                constraint_list.append(AllDiffConstraint(name, scope))

    vars = [var for row in var_array for var in row]
    return CSP("Sudoku", vars, constraint_list)


def post_all_pairs(var_list):
    '''create a not equal constraint between all pairs of variables in var_list
       return list of constructed constraint objects'''
    constraints = []
    for i in range(len(var_list)):
        for j in range(i + 1, len(var_list)):
            c = NeqConstraint(
                "({},{})".format(var_list[i].name(), var_list[j].name()),
                [var_list[i], var_list[j]])
            constraints.append(c)
    return constraints


def solve_sudoku(initialBoard, model, algo, allsolns,
                 variableHeuristic='fixed', trace=False):
    if not model in ['neq', 'alldiff']:
        print("Error wrong sudoku model specified {}. Must be one of {}".format(
            model, ['neq', 'alldiff']))
    csp = sudokuCSP(initialBoard, model)

    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns,
                                     trace)
    print("Explored {} nodes".format(num_nodes))
    if len(solutions) == 0:
        print("No solutions to {} found".format(csp.name()))
    else:
        i = 0
        for s in solutions:
            i += 1
            print("Solution #{}: ".format(i))
            sudoku_print_soln(s)


def sudoku_print_soln(s):
    '''s is a list of (var,value) pairs. Organize them into
       the right order and then print(it in a board layout'''
    s.sort(key=lambda varval_pair: varval_pair[0].name())
    print("-" * 37)
    for i in range(0, 9):
        print("|", end='')
        for j in range(0, 9):
            indx = i * 9 + j
            print(s[indx][1], "|", end='')
        print("")
        print("-" * 37)


##################################################################
### Plane Sequencing
##################################################################

class PlaneProblem:
    '''Class to hold an instance of the plane scheduling problem.
       defined by the following data items
       a) A list of planes

       b) A list of needed flights

       c) Legal flights for each plane. Specified as a list of lists
          For each list L. L[0] = a particular plane P. and L[1], L[2} ...
          are all of the flights that P is equipped to fly.
          This must be a subset of the list of flights

       d) Possible starting flights for each plane. Specified as a
          list of lists For each list L. L[0] = a particular plane P,
          and L[1], L[2], ...  are all of the flights that in the same
          place the plane that P is initially located. This must be a
          subset of the list of flights. Note however, that that P
          might not be able to fly all of these flights (so the list
          (c) needs to be checked as well)


       e) A list of pairs of flights (f1,f2) such that f2 can legally
          follow f1 in a plane's schedule. (That is, f2 starts at the
          same location that f1 end).

       f) A list of flights that end in a location where maintenance
          can be performed

       g) In integer specifying the minimum frequency of plane
          maintenance. That is, if the minimum frequency is 4, then at
          least one out of every sequence of 4 flights a plane makes
          must be a flight ending at a location where maintenance can
          be performed.

    '''

    def __init__(self, planes, flights, can_fly, flights_at_start,
                 can_follow, maintenance_flights, min_maintenance_frequency):
        self.planes = planes
        self.flights = flights
        self._can_fly = dict()
        self._flights_at_start = dict()
        self.can_follow = can_follow
        self.maintenance_flights = maintenance_flights
        self.min_maintenance_frequency = min_maintenance_frequency

        # do some data checks
        for l in can_fly:
            for f in l[1:]:
                if f not in flights:
                    print("PlaneProblem Error, can_fly contains a non-flight",
                          f)
        for l in flights_at_start:
            for f in l[1:]:
                if f not in flights:
                    print(
                        "PplaneProblem Error, flights_at_start contains a non-flight",
                        f)
        for (f1, f2) in can_follow:
            if f1 not in flights or f2 not in flights:
                print(
                    "PlaneProblem Error, can_fly contains pair with non-flight (",
                    f1, ",", f2, ")")

        for f in maintenance_flights:
            if f not in flights:
                print(
                    "PlaneProblem Error, maintenance_flights fly contains non-flight",
                    f)

        if min_maintenance_frequency == 0:
            print(
                "PlaneProblem Error, min_maintenance_frequency must be greater than 0")

        # now convert can_fly and flights_at_start to a dictionary that
        # can be indexed by the plane.
        for l in can_fly:
            self._can_fly[l[0]] = l[1:]
        for l in flights_at_start:
            self._flights_at_start[l[0]] = l[1:]

        # some useful access functions

    def can_fly(self, plane):
        '''Return list of flights plane can fly'''
        return self._can_fly[plane]

    def can_start(self, plane):
        '''Return list of flights plane can start with'''
        return list(
            set(self._can_fly[plane]).intersection(
                self._flights_at_start[plane]))


def solve_planes(planes_problem, algo, allsolns,
                 variableHeuristic='fixed', silent=False, trace=False):
    # Your implementation for Question 6 goes here.
    #
    # Do not but do not change the functions signature
    # (the autograder will twig out if you do).

    # If the silent parameter is set to True
    # you must ensure that you do not execute any print statements
    # in this function.
    # (else the output of the autograder will become confusing).
    # So if you have any debugging print statements make sure you
    # only execute them "if not silent". (The autograder will call
    # this function with silent=True, plane_scheduling.py will call
    # this function with silent=False)

    # You can optionally ignore the trace parameter
    # If you implemented tracing in your FC and GAC implementations
    # you can set this argument to True for debugging.
    #
    # Once you have implemented this function you should be able to
    # run plane_scheduling.py to solve the test problems (or the autograder).
    #
    #
    '''This function takes a planes_problem (an instance of PlaneProblem
       class) as input. It constructs a CSP, solves the CSP with bt_search
       (using the options passed to it), and then from the set of CSP
       solutions it constructs a list of lists specifying a schedule
       for each plane and returns that list of lists
       The required format is the list of lists is:

       For each plane P the list of lists contains a list L.
       L[0] == P (i.e., the first item of the list is the plane)
       and L[1], ..., L[k] (i.e., L[1:]) is the sequence of flights
       assigned to P.

       The returned list of lists should contain a list for every
       plane.
    '''

    # BUILD your CSP here and store it in the varable csp
    constr_lst = []
    planes_dic = {}
    var_lst = []
        # To check constrains 1,2
    for plane in planes_problem.planes:
        can_start = planes_problem.can_start(plane) + [',']

        start_var = Variable("Plane:{}_1".format(plane), can_start)
        planes_dic[plane] = [start_var]

        plane_can_fly = planes_problem.can_fly(plane) + [',']

        for i in range(2, len(plane_can_fly)):
            fly = Variable("Plane:{}_{}".format(plane, i), plane_can_fly)
            planes_dic[plane].extend([fly])

        var_lst.extend(planes_dic[plane])

        # To check constrains 3

        follow = []
        for (flight1, flight2) in planes_problem.can_follow:
            if flight1 in plane_can_fly and flight2 in plane_can_fly:
                follow.append([flight1, flight2])
        for flight in plane_can_fly:
            follow.append([flight, ','])

        col = planes_dic[plane]

        for i in range(len(col) - 1):
            name = "Plane_{}_({}_{})".format(plane, i+1, i+2)
            scope = [col[i], col[i+1]]
            constr_table = TableConstraint(name, scope, follow)
            constr_lst.append(constr_table)

        # To check constrains 4

        maintainable = []
        maintenance_frequency = planes_problem.min_maintenance_frequency
        for maintenance_flight in planes_problem.maintenance_flights:
            if maintenance_flight in plane_can_fly:
                maintainable.append(maintenance_flight)

        for i in range(len(col) - maintenance_frequency + 1):
            name = "Plane_{}_R({},{})".format(plane, i + 1, i + maintenance_frequency)
            scope = []
            required_value = maintainable + [',']
            for j in range(i, i+maintenance_frequency):
                scope.append(col[j])

            maint_const = NValuesConstraint(name, scope, required_value, 1,  maintenance_frequency)
            constr_lst.append(maint_const)

    # To check constrains 5
    for flight in planes_problem.flights:
        name = "Flight_{}".format(flight)
        flight_constrain = NValuesConstraint(name, var_lst, [flight], 1, 1)
        constr_lst.append(flight_constrain)

    csp = CSP("Plane", var_lst, constr_lst)
    # invoke search with the passed parameters
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns,
                                     trace)
    result = []
    for sol in solutions:

        sol_dic = {}
        for plane in planes_problem.planes:
            sol_dic[plane] = []

        for (var, val) in sol:
            var_name = var.name()
            row = int(var_name.split("_")[1])
            plane = var_name.split(":")[1].split("_")[0]
            sol_dic[plane].append((row, val))

        inOder_sol_dic = {}
        for plane in sol_dic:
            sol_dic[plane].sort()
            inOder_sol_dic[plane] = []
            for step in sol_dic[plane]:
                if step[1] != ",":
                    inOder_sol_dic[plane].append(step[1])

        sol = []
        for plane in inOder_sol_dic:
            sol.append([plane] + inOder_sol_dic[plane])
        result.append(sol)
    return result




    # Convert each solution into a list of lists specifying a schedule
    # for each plane in the format described above.

    # then return a list containing all converted solutions
    # (i.e., a list of lists of lists)
