import Functions.Parser as Parser
from Functions.ProcessFile import process
import pip


def install(package):
    pip.main(['install', package])


try:
    from IPython.display import FileLink
except ImportError:
    print('Ipython is not installed, installing it now!')
    install('IPython')

try:
    import csv
except ImportError:
    print('csv is not installed, installing it now!')
    install('csv')

try:
    import os
except ImportError:
    print('os is not installed, installing it now!')
    install('os')

algs = ["Brute Force", "WALKSAT (LOCAL_SEARCH)", "DPLL", "Constraint_Programming (Ortools)", "CDCL (GLucose3)"]


def getLiterals(clauses):
    return set([abs(y) for x in clauses for y in x])


def submission_generation(filename, str_output):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in str_output:
            writer.writerow(item)
    return FileLink(filename)


def printVerbose(file, info, clauses, times, algot, value):
    print("Total variables calculadas:", len(getLiterals(clauses)), "| Total variables dichas:",
          info.get("variables"))
    print("Fichero -->", file, "| Valor -->", value)
    print("Algoritmo requerido:", algs[algot - 1], "| Tiempo requerido -->", times)
    print("------------------------------------------------------------------------")


def main(ifile, nameFile, algot):
    nameFileRes = "resultado.csv"

    str_output = [[algs[algot-1]], ["Filename", "Value", "Time in seconds"]]

    if ifile == 2:
        is_file, file = Parser.checkFile(nameFile)

        if not is_file:
            times = 0
            for dirname, _, filenames in os.walk(file):
                for filename in filenames:
                    if dirname[-1] == "/":
                        full_name = dirname + filename
                    else:
                        full_name = dirname + '/' + filename

                    with open(full_name, 'r') as input_data_file:
                        data_lines = [a.rstrip("\r\n") for a in input_data_file]
                        clauses, info = Parser.parserFile(data_lines)

                        assert len(clauses) == info.get("clausulas"), "Parseo incorrecto->clausulas"

                        value, time, dictSol = process(clauses, algot)
                        times += time
                        str_output.append([full_name, value, times])

            print("Se ha generado el fichero de salida:", nameFileRes)
            submission_generation(nameFileRes, str_output)
            return None, times, nameFileRes
        else:
            with open(file, 'r') as input_data_file:
                data_lines = [a.rstrip("\r\n") for a in input_data_file]
                clauses, info = Parser.parserFile(data_lines)

                assert len(clauses) == info.get("clausulas"), "Parseo incorrecto->clausulas"

                value, times, dictSol = process(clauses, algot)

                str_output.append([file, value, times])
    else:
        litDict, clauses = Parser.parserFormula(nameFile)
        value, times, dictS = process(clauses, algot)
        str_output.append([nameFile, value, times])
        if dictS:
            dictSol = dict(zip(litDict.keys(), dictS.values()))
        else:
            dictSol = None

    print("Se ha generado el fichero de salida:", nameFileRes)
    submission_generation(nameFileRes, str_output)
    if value == "UNSATISFIABLE":
        return False, times, dictSol
    else:
        return True, times, dictSol



