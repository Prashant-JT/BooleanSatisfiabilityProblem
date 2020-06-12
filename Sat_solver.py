from pysat.solvers import Glucose3
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
        au = -values[abs(ax)-1]
    else:
        au = values[abs(ax)-1]
    return True if au > 0 else False


def check_solution(values, clauses):

    sol = True
    for unit in clauses:
        aux = True
        for i in unit:
            aux = aux or convertBool(values, i)
        sol = sol and aux

    return "SATISFIABLE" if sol else "ERROR------------"


def process(clauses):

    g = Glucose3()
    for cl in clauses:
        g.add_clause(cl)

    a = g.solve()

    return check_solution(g.get_model(), clauses) if a else "UNSATISFIABLE"


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
    return claus, list(literals), claus_var


def main():
    for dirname, _, filenames in os.walk('./data'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    str_output = [["Filename", "Value"]]
    counter = 0
    for dirname, _, filenames in os.walk('./data'):
        for filename in filenames:
            full_name = dirname+'/'+filename
            with open(full_name, 'r') as input_data_file:

                data_lines = [a.rstrip("\r\n") for a in input_data_file]
                clauses, liter, info = parserFile(data_lines)

                assert len(clauses) == info.get("clausulas"), "Parseo incorrecto->clausulas"
                print("Total variables calculadas:", len(liter), "| Total variables dichas:", info.get("variables"))

                value = process(clauses)

                print("Fichero -->", filename, '(', dirname[7:], ") | Valor -->", value)
                print("------------------------------------------------------------------------")
                str_output.append([filename, value])

            counter += 1

    sortedlist = sorted(str_output, key=lambda row: row[0], reverse=False)
    submission_generation('SAT.csv', sortedlist)


if __name__ == '__main__':
    main()
