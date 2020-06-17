import pip


def install(package):
    pip.main(['install', package])


try:
    from pysat.solvers import Glucose3
except ImportError:
    print('usertools is not installed, installing it now!')
    install('python-sat[pblib,aiger]')


class CDCL:

    sat = False
    satDict = None

    def __init__(self, clauses):
        self.clauses = clauses

    def getLiterals(self):
        return set([abs(y) for x in self.clauses for y in x])

    def solve(self):
        literals = CDCL.getLiterals(self)
        n = max(literals) + 1

        g = Glucose3()
        for cl in self.clauses:
            g.add_clause(cl)

        self.sat = g.solve()
        if self.sat:
            self.satDict = dict(zip(range(1, n), [True if x > 0 else False for x in g.get_model()]))
