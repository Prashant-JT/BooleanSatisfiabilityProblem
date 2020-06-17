import getopt
import os
import re
import sys


def checkFile(file):
    if os.path.isfile(file):
        return True, file
    elif os.path.isdir(file):
        return False, file
    print("El fichero o directorio no existe")
    sys.exit(1)


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

