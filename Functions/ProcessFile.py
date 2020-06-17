import pip
from Algos.BruteForce import BruteForce
from Algos.DPLL import solve as DPLLsolve
from Algos.CP_SAT import ConstProg
from Algos.WalkSat import WalkSat
from Algos.CDCL import CDCL


def install(package):
    pip.main(['install', package])


try:
    import time
except ImportError:
    print('time is not installed, installing it now!')
    install('time')


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

    return "SATISFIABLE" if sol else "UNSATISFIABLE"


def algorythms(clauses, algos):
    if algos == 1:
        bf = BruteForce(clauses)
        bf.solve()
        return bf.sat, bf.satDict
    elif algos == 2:
        wks = WalkSat(clauses)
        wks.solve()
        return wks.sat, wks.satDict
    elif algos == 3:
        return DPLLsolve(clauses)  # Complejidad recursiva, sin clase
    elif algos == 4:
        cpsat = ConstProg(clauses)
        cpsat.solve()
        return cpsat.sat, cpsat.satDict
    else:
        cdcl = CDCL(clauses)
        cdcl.solve()
        return cdcl.sat, cdcl.satDict


def process(clauses, algos):
    start = time.time()
    val, dictSol = algorythms(clauses, algos)
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

        return obj, end - start, dictSol
