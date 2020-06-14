import itertools
import random
import sys
import time
from IPython.display import FileLink
import csv
import os
import re
import gurobipy as gp
from gurobipy import GRB


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


def grb_SAT(clauses):
    n = max(getLiterals(clauses))+1
    literals = range(1, n)

    model = gp.Model("MIP_SAT")
    Lit = model.addVars(literals, vtype=GRB.BINARY, name="X")
    NotLit = model.addVars(literals, vtype=GRB.BINARY, name="NotX")

    Cla = model.addVars(len(clauses), vtype=GRB.BINARY, name="Clause")

    Obj0 = model.addVar(vtype=GRB.BINARY, name="Obj0")
    Obj1 = model.addVar(vtype=GRB.BINARY, name="Obj1")

    # Link Xi and notXi
    model.addConstrs((Lit[i] + NotLit[i] == 1.0 for i in literals), name="CNSTR_X")

    # Link clauses and literals
    for i, c in enumerate(clauses):
        clause = []
        for l in c:
            if l < 0:
                clause.append(NotLit[abs(l)])
            else:
                clause.append(Lit[l])
        model.addConstr(Cla[i] == gp.or_(clause), "CNSTR_Clause" + str(i))

    # Link objs with clauses
    model.addConstr(Obj0 == gp.min_(Cla), name="CNSTR_Obj0")
    model.addConstr((Obj1 == 1) >> (Cla.sum() >= n), name="CNSTR_Obj1")

    # Set optimization objective
    model.setObjective(Obj0 + Obj1, GRB.MAXIMIZE)

    # Optimize
    model.optimize()

    # Print result
    objval = model.getAttr(GRB.Attr.ObjVal)

    if objval > 1.9:
        solution = {}
        for key, value in model.getAttr(Lit).items():
            solution[key] = True if value > 0.9 else False
        return True, solution
    else:
        return False, None


"""
-------------FIN ALGORITMOS------------
"""

algos = 4
algs = ["Fuerza bruta", "DPLL", "WALKSAT (LOCAL_SEARCH)", "MIP", "SOLVER_SAT(CDCL)"]


def getLiterals(clauses):
    return set([abs(y) for x in clauses for y in x])


def algorythms(clauses):

    return grb_SAT(clauses)


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
