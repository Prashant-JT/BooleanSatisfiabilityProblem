import pip


def install(package):
    pip.main(['install', package])


try:
    from ortools.sat.python import cp_model
except ImportError:
    print('usertools is not installed, installing it now!')
    install('ortools')


class ConstProg:
    sat = False
    satDict = {}

    def __init__(self, clauses):
        self.clauses = clauses

    def getLiterals(self):
        return set([abs(y) for x in self.clauses for y in x])

    def solve(self):
        n = max(ConstProg.getLiterals(self)) + 1
        literals = range(1, n)
        boolLit = [0]

        model = cp_model.CpModel()

        for x in literals:
            boolLit.append(model.NewBoolVar(str(x)))

        for cl in self.clauses:
            cl_rep = [boolLit[a] if a > 0 else boolLit[abs(a)].Not() for a in cl]
            model.AddBoolOr(cl_rep)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            boolLit.remove(0)
            for x, y in zip(literals, boolLit):
                self.satDict[x] = True if solver.Value(y) == 1 else False
            if status == cp_model.OPTIMAL:
                self.sat = True
        else:
            self.satDict = None
