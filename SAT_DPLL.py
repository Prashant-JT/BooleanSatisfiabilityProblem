import itertools
from pysat.solvers import Glucose3
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


def brute_force(clauses, literals):
    n = len(literals)

    for seq in itertools.product([True, False], repeat=n):
        res = set([lit if boo else -lit for boo, lit in zip(seq, literals)])
        if all([bool(set(x).intersection(res)) for x in clauses]):
            return True, dict(zip(range(1, n+1), seq))

    return False, None


def dpll(cnf, assignments={}):
    if len(cnf) == 0:
        return True, assignments

    if any([len(c) == 0 for c in cnf]):
        return False, None

    l = (cnf[0])[0]

    def diff(first, second):
        return list(set(first) - set(second))

    new_cnf = [c for c in cnf if l not in c]
    new_cnf = [diff(c, [-l]) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals

    new_cnf = [c for c in cnf if -l not in c]
    new_cnf = [diff(c, [l]) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals

    return False, None


def solver_SAT_CDCL(clauses, n):
    g = Glucose3()
    for cl in clauses:
        g.add_clause(cl)

    a = g.solve()
    b = dict(zip(range(1, n), [True if x > 0 else False for x in g.get_model()])) if a else None
    return a, b


"""
-------------FIN ALGORITMOS------------
"""

algos = 3
algs = ["Fuerza bruta", "DPLL", "SOLVER_SAT(CDCL)"]


def algorythms(alg, clauses, literals):
    if alg == 1:
        return brute_force(clauses, literals)
    elif alg == 2:
        return dpll(clauses, {})
    else:
        return solver_SAT_CDCL(clauses, max(literals)+1)


def process(clauses, literals, alg):
    start = time.time()
    val, dictSol = algorythms(alg, clauses, literals)
    end = time.time()

    obj = "UNSATISFIABLE"

    if val:
        sol = [0] * len(dictSol)
        for key, value in dictSol.items():
            sol[abs(key) - 1] = key if value else -key

        obj = check_solution(sol, clauses)

    aux = True if obj == "SATISFIABLE" else False
    assert val == aux

    return obj, end-start


def parserFile(datas):
    claus = []
    literals = set()
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
            literals.update((abs(x) for x in auxS))
    return claus, literals, claus_var


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
                clauses, liter, info = parserFile(data_lines)

                assert len(clauses) == info.get("clausulas"), "Parseo incorrecto->clausulas"
                print("Total variables calculadas:", len(liter), "| Total variables dichas:", info.get("variables"))

                value, times = process(clauses, liter, algos)

                print("Fichero -->", filename, '(', dirname[7:], ") | Valor -->", value)
                print("Algoritmo requerido:", algs[algos-1], "| Tiempo requerido -->", times)
                print("------------------------------------------------------------------------")
                str_output.append([filename, value])

            counter += 1

    sortedlist = sorted(str_output, key=lambda row: row[0], reverse=False)
    submission_generation('SAT.csv', sortedlist)


if __name__ == '__main__':
    main()
