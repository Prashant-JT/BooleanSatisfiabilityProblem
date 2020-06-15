import itertools
import random
from pysat.solvers import Glucose3
from ortools.sat.python import cp_model
import time
from IPython.display import FileLink
import csv
import os
import re


def submission_generation(filename, str_output):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in str_output:
            writer.writerow(item)
    return FileLink(filename)


def convertBool(values, ax):
    if ax < 0:
        au = -values[abs(ax) - 1]
    else:
        au = values[abs(ax) - 1]
    return True if au > 0 else False


def check_solution(values, clauses):
    sol = True
    for unit in clauses:
        aux = False
        for i in unit:
            aux = aux or convertBool(values, i)
        sol = sol and aux

    return "SATISFIABLE" if sol else "ERROR------------"


"""
---------------ALGORITMOS--------------
"""


def brute_force(clauses):
    literals = getLiterals(clauses)
    n = len(literals)

    for seq in itertools.product([True, False], repeat=n):
        res = set([lit if boo else -lit for boo, lit in zip(seq, literals)])
        if all([bool(set(x).intersection(res)) for x in clauses]):
            return True, dict(zip(literals, seq))

    return False, None


"""
---------DPLL--------
"""


def bcp(clauses, unit):
    clausX = []
    for cl in clauses:
        if unit in cl:
            continue
        if -unit in cl:
            new_cl = [x for x in cl if x != -unit]
            if not new_cl:
                return -1
            clausX.append(new_cl)
        else:
            clausX.append(cl)
    return clausX


def pure_literal(clauses):
    literals = set([y for x in clauses for y in x])
    assign = []
    pures = [x for x in literals if -x not in literals]
    for pure in pures:
        clauses = bcp(clauses, pure)
    assign += pures
    return clauses, assign


def unit_propagation(clauses):
    assign = []
    units = [c for c in clauses if len(c) == 1]
    while units:
        unit = (units[0])[0]
        clauses = bcp(clauses, unit)
        assign.append(unit)
        if clauses == -1:
            return -1, []
        if not clauses:
            return clauses, assign
        units = [c for c in clauses if len(c) == 1]
    return clauses, assign


def jeroslow_wang_2_sided(clauses, weight=2):
    aux = {}
    for cl in clauses:
        for lit in cl:
            # Siendo weight=2, len(cl)=3 -> 2^(-3)=0.125
            if abs(lit) in aux:
                aux[abs(lit)] += weight ** -len(cl)
            else:
                aux[abs(lit)] = weight ** -len(cl)
    return aux


def heuristic_selector(clauses):
    # Se devuelve aquel literal que tenga un mayor valor.
    aux = jeroslow_wang_2_sided(clauses)
    return max(aux, key=aux.get)


def dpll(clauses, assign):
    clauses, pure_assignment = pure_literal(clauses)
    clauses, unit_assignment = unit_propagation(clauses)
    assign.extend(pure_assignment + unit_assignment)

    if clauses == - 1:
        return []
    if not clauses:
        return assign

    variable = heuristic_selector(clauses)
    solution = dpll(bcp(clauses, variable), assign + [variable])
    if not solution:
        solution = dpll(bcp(clauses, -variable), assign + [-variable])
    return solution


def dpll_aux(clauses):
    literals = getLiterals(clauses)

    res = dpll(clauses, [])
    if res:
        res.extend([x for x in literals if x not in res and -x not in res])
        res.sort(key=lambda x: abs(x))
        return True, dict(zip(literals, [True if x > 0 else False for x in res]))
    else:
        return False, None


"""
--------FIN DPLL-------
"""


def mip_SAT(clauses):
    n = max(getLiterals(clauses)) + 1
    literals = range(1, n)
    boolLit = [0]

    model = cp_model.CpModel()

    for x in literals:
        boolLit.append(model.NewBoolVar(str(x)))

    for cl in clauses:
        cl_rep = [boolLit[a] if a > 0 else boolLit[abs(a)].Not() for a in cl]
        model.AddBoolOr(cl_rep)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        sol = {}
        boolLit.remove(0)
        for x, y in zip(literals, boolLit):
            sol[x] = True if solver.Value(y) == 1 else False
        if status == cp_model.OPTIMAL:
            return True, sol
        else:
            return False, sol
    else:
        return False, None


"""
--------WALKSAT (LOCAL-SEARCH)---------
"""


def checkSAT(cl, assign):
    for c in cl:
        if assign[abs(c)] and c > 0:
            return True
        elif not assign[abs(c)] and c < 0:
            return True
    return False


def check(clauses, assign):
    for cl in clauses:
        if not checkSAT(cl, assign):
            return False
    return True


def walksat(clauses, max_flips, p, limit):
    literals = getLiterals(clauses)
    assign = {s: random.choice([True, False]) for s in literals}

    while limit:
        for _ in range(max_flips):

            if check(clauses, assign):
                return assign

            cl = random.choice(clauses)
            while not checkSAT(cl, assign):
                cl = random.choice(clauses)

            r = random.uniform(0, 1) < p
            if r:
                lit = abs(random.choice(cl))
                assign[lit] = not assign[lit]
            else:
                flip = 0
                satClauses = 0
                for symb in cl:
                    mod = assign.copy()
                    mod[abs(symb)] = not mod[abs(symb)]

                    j = 0
                    for claus in clauses:
                        if checkSAT(claus, mod):
                            j += 1

                    if j > satClauses:
                        satClauses = j
                        flip = abs(symb)

                assign[flip] = not assign[flip]
        limit -= 1
    return False


def walksat_aux(clauses):
    max_flips = 50000
    p = 0.6
    res = walksat(clauses, max_flips, p, 5)

    if res:
        return True, res
    else:
        return False, None


"""
-------FIN WALKSAT---------
"""


def solver_SAT_CDCL(clauses):
    literals = getLiterals(clauses)
    n = max(literals) + 1

    g = Glucose3()
    for cl in clauses:
        g.add_clause(cl)

    a = g.solve()
    b = dict(zip(range(1, n), [True if x > 0 else False for x in g.get_model()])) if a else None
    return a, b


"""
-------------FIN ALGORITMOS------------
"""

algos = 4
algs = ["Brute Force", "DPLL", "WALKSAT (LOCAL_SEARCH)", "MIP with ORTOOLS", "SOLVER_SAT(CDCL)"]


def getLiterals(clauses):
    return set([abs(y) for x in clauses for y in x])


def algorythms(clauses):
    global algos
    if algos == 1:
        return brute_force(clauses)
    elif algos == 2:
        return dpll_aux(clauses)
    elif algos == 3:
        return walksat_aux(clauses)
    elif algos == 4:
        return mip_SAT(clauses)
    else:
        return solver_SAT_CDCL(clauses)


def process(clauses):
    global algos
    start = time.time()
    val, dictSol = algorythms(clauses)
    end = time.time()

    obj = "UNSATISFIABLE" if algos != 3 else "UNKNOWN"

    if val:
        sol = [0] * len(dictSol)
        for key, value in dictSol.items():
            sol[abs(key) - 1] = abs(key) if value else -abs(key)

        obj = check_solution(sol, clauses)

    if not val and dictSol:
        return obj, end - start
    else:
        aux = True if obj == "SATISFIABLE" else False
        assert val == aux

        return obj, end - start


def parserFile(datas):
    claus = []
    claus_var = {}
    for line in datas:
        comment = re.match("p.+", line)
        clause = re.match("\\s*-?[1-9]+.*[^0]", line)

        if comment:
            auxC = comment.group().split()
            # print("--------------------------------------------------------------")
            if len(auxC) > 3:
                claus_var["variables"] = int(auxC[2])
                claus_var["clausulas"] = int(auxC[3])
                # print("Número de variables:", auxC[2], "| Número de claúsulas:", auxC[3])

        if clause:
            auxS = [int(i) for i in clause.group().split()]
            claus.append(auxS)
    return claus, claus_var


def main():
    global algos, algs
    for dirname, _, filenames in os.walk('./data'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    str_output = [["Filename", "Value"]]
    counter = 0
    for dirname, _, filenames in os.walk('./data'):
        for filename in filenames:
            full_name = dirname + '/' + filename
            with open(full_name, 'r') as input_data_file:
                data_lines = [a.rstrip("\r\n") for a in input_data_file]
                clauses, info = parserFile(data_lines)

                assert len(clauses) == info.get("clausulas"), "Parseo incorrecto->clausulas"
                print("Total variables calculadas:", len(getLiterals(clauses)), "| Total variables dichas:", info.get("variables"))

                value, times = process(clauses)

                print("Fichero -->", filename, '(', dirname[7:], ") | Valor -->", value)
                print("Algoritmo requerido:", algs[algos - 1], "| Tiempo requerido -->", times)
                print("------------------------------------------------------------------------")
                str_output.append([filename, value])

            counter += 1

    sortedlist = sorted(str_output, key=lambda row: row[0], reverse=False)
    submission_generation('SAT.csv', sortedlist)


if __name__ == '__main__':
    main()
