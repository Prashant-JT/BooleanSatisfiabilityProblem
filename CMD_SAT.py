import csv
import os
import sys
import Functions.Parser as Parser
from Functions.ProcessFile import process
from IPython.display import FileLink

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


def main(argv):
    file, algot, outF, verbose, is_file, equals = Parser.parserArgs(argv)

    str_output = [["Filename", "Value", "Time in seconds"]]

    def processRead(files):
        with open(files, 'r') as input_data_file:
            data_lines = [a.rstrip("\r\n") for a in input_data_file]
            clauses, info = Parser.parserFile(data_lines)

            assert len(clauses) == info.get("clausulas"), "Parseo incorrecto->clausulas"

            value, times, dictSol = process(clauses, algot)

            if verbose:
                printVerbose(files, info, clauses, times, algot, value)

            str_output.append([files, value, times])

            if value and equals:
                str_res = [["Variable", "Value"]]
                for key_, value_ in dictSol.items():
                    str_res.append([key_, value_])
                print("Se ha generado el fichero de resultados:", outF + '_res.csv')
                submission_generation(outF + '_res.csv', str_res)

    if not is_file:
        for dirname, _, filenames in os.walk(file):
            for filename in filenames:
                if dirname[-1] == "/":
                    full_name = dirname + filename
                else:
                    full_name = dirname + '/' + filename

                processRead(full_name)
    else:
        processRead(file)

    print("Se ha generado el fichero de salida:", outF + '.csv')
    submission_generation(outF + '.csv', str_output)


if __name__ == '__main__':
    if len(sys.argv) < 5 and ("-h" not in sys.argv):
        print("Se requieren más argumentos")
        Parser.helpMessage()
        sys.exit(1)
    main(sys.argv[1:])
