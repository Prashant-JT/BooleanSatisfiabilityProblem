import pip


def install(package):
    pip.main(['install', package])


try:
    import itertools
except ImportError:
    print('itertools is not installed, installing it now!')
    install('itertools')


class BruteForce:

    sat = False
    satDict = None

    def __init__(self, clauses):
        self.clauses = clauses

    def getLiterals(self):
        return set([abs(y) for x in self.clauses for y in x])

    def solve(self):
        literals = BruteForce.getLiterals(self)
        n = len(literals)

        for seq in itertools.product([True, False], repeat=n):
            res = set([lit if boo else -lit for boo, lit in zip(seq, literals)])
            if all([bool(set(x).intersection(res)) for x in self.clauses]):
                self.sat, self.satDict = True, dict(zip(literals, seq))
