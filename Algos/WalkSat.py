import pip


def install(package):
    pip.main(['install', package])


try:
    import random
except ImportError:
    print('random is not installed, installing it now!')
    install('random')


def checkSAT(cl, assign):
    for c in cl:
        if assign[abs(c)] and c > 0:
            return True
        elif not assign[abs(c)] and c < 0:
            return True
    return False


class WalkSat:

    sat = False
    satDict = None

    def __init__(self, clauses):
        self.clauses = clauses

    def getLiterals(self):
        return set([abs(y) for x in self.clauses for y in x])

    def check(self, clauses):
        for cl in clauses:
            if not checkSAT(cl, self.satDict):
                return False
        return True

    def walkSat(self, max_flips, p, limit):
        literals = WalkSat.getLiterals(self)
        self.satDict = {s: random.choice([True, False]) for s in literals}

        while limit:
            for _ in range(max_flips):

                if WalkSat.check(self, self.clauses):
                    return self.satDict

                cl = random.choice(self.clauses)
                while not checkSAT(cl, self.satDict):
                    cl = random.choice(self.clauses)

                r = random.uniform(0, 1) < p
                if r:
                    lit = abs(random.choice(cl))
                    self.satDict[lit] = not self.satDict[lit]
                else:
                    flip = 0
                    satClauses = 0
                    for symb in cl:
                        mod = self.satDict.copy()
                        mod[abs(symb)] = not mod[abs(symb)]

                        j = 0
                        for claus in self.clauses:
                            if checkSAT(claus, mod):
                                j += 1

                        if j > satClauses:
                            satClauses = j
                            flip = abs(symb)

                    self.satDict[flip] = not self.satDict[flip]
            limit -= 1
        return False

    def solve(self):
        max_flips = 50000
        p = 0.6
        limit = 5

        if WalkSat.walkSat(self, max_flips, p, limit):
            self.sat = True
        else:
            self.sat = False
