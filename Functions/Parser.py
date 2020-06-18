import pip


def install_packages(package):
    pip.main(['install', package])


try:
    import re, sys, os, getopt
except ImportError:
    print('re & os is not installed, installing it now!')
    install_packages('re')
    install_packages('sys')
    install_packages('os')
    install_packages('getopt')


def helpMessage():
    hMessage = "***Usage: python3 " + sys.argv[0] + " -i [<inputFile>|<inputDirectory>] -[a <keyAlgorythms>] " \
                                                    "-o <outputFile> -[h|v|e]***"
    eMessage = "Use option 'e' to generate another file with values, only for files"
    aMessage = "Algorythms = {1: Brute_Force, 2: WALKSAT (LOCAL_SEARCH), 3: DPLL, " \
               "4: Constraint_Programming (Ortools), 5: CDCL (GLucose3)}"
    print(hMessage, "\n")
    print(eMessage, "\n")
    print(aMessage)


def parserArgs(argv):
    try:
        opts, args = getopt.getopt(argv, "i:o:hvea:")
    except getopt.GetoptError:
        helpMessage()
        sys.exit(2)

    file = outF = ""
    algot = 5
    verbose = directory = equals = False

    for opt, arg in opts:
        if opt == "-h":
            helpMessage()
            sys.exit(0)
        elif opt == "-i":
            directory, file = checkFile(arg)
            if directory is None:
                sys.exit(1)
        elif opt == "-a":
            if not arg.isdigit():
                print("Algoritmo inexistente, los algoritmos deben ser numéricos")
                helpMessage()
                sys.exit(1)
            algot = int(arg)
            if algot < 1 or algot > 5:
                print("Algoritmo inexistente, pruebe de 1 a 5, ambos inclusive")
                helpMessage()
                sys.exit(1)
        elif opt == "-e":
            equals = True
        elif opt == "-v":
            verbose = True
        elif opt == "-o":
            outF = arg
        else:
            helpMessage()
            sys.exit(0)

    return file, algot, outF, verbose, directory, equals


def checkFile(file):
    if os.path.isfile(file):
        return True, file
    elif os.path.isdir(file):
        return False, file
    print("El fichero o directorio no existe")
    return None, None


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


def parserFormula(formula):
    litDict = {}
    clauses = []
    if formula.find("(", 1) != -1 and "," not in formula:
        print("Formula incorrecta, los espaciadores son ','")
        return None, None
    try:
        cont = 1
        for cl in formula.split(','):
            if cl.find('(') != 0 and cl.find(')') != len(cl)-1:
                print("Formula incorrecta, cada clausula debe estar entre '()'")
                return None, None
            auxC = []
            for a in cl[1:-1].split('+'):
                b = a.replace("!", "")
                if b not in litDict:
                    litDict[b] = cont
                    cont += 1
                auxC.append(litDict[b] if a[0] != "!" else -litDict[b])
            clauses.append(auxC)
    except Exception:
        print("Clausula invalida, vuelva a intentarlo")
        return None, None

    return litDict, clauses




