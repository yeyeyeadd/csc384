var_lst = []
planes_dic = {}
constr_lst = []
for plane in planes_problem.planes:
    can_start = planes_problem.can_start(plane) + ['END']

    start_var = Variable("Plane:{}_1".format(plane), can_start)
    planes_dic[plane] = [start_var]

    can_fly = planes_problem.can_fly(plane) + ['END']

    for i in range(2, len(can_fly)):
        fly = Variable("Plane:{}_{}".format(plane, i), can_fly)
        planes_dic[plane].extend([fly])

    var_lst.extend(planes_dic[plane])

    # To check constrains 3
    follow = []
    for (flight1, flight2) in planes_problem.can_follow:
        if flight1 in can_fly and flight2 in can_fly:
            follow.append([flight1, flight2])
    for flight in can_fly:
        follow.append([flight, 'END'])

    col = planes_dic[plane]

    for i in range(len(col) - 1):
        name = "Plane_{}_({}_{})".format(plane, i+1, i+2)
        scope = [col[i], col[i+1]]
        constr_table = TableConstraint(name, scope, follow)
        constr_lst.append(constr_table)

    #To check constrains 4

    maintainable = []
    maintenance_frequency = planes_problem.min_maintenance_frequency
    for maintenance_flight in planes_problem.maintenance_flights:
        if maintenance_flight in can_fly:
            maintainable.append(maintenance_flight)

    for i in range(len(col) - maintenance_frequency + 1):
        name = "Plane_{}_R({},{})".format(plane, i + 1, i + maintenance_frequency)
        scope = []
        required_value = maintainable + ['END']
        for j in range(i, i+maintenance_frequency):
            scope.append(col[j])

        maint_const = NValuesConstraint(name, scope, required_value, 1,  maintenance_frequency)
        constr_lst.append(maint_const)

    #TO check constrains 5
    for flight in planes_problem.flights:
        name = "Flight_{}".format(flight)
        flight_constr = NValuesConstraint(name, var_lst, [flight], 1, 1)
        constr_lst.append(flight_constr)

csp = CSP("Plane", var_lst,  constr_lst)
