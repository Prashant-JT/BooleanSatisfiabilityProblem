
def getLiterals(clauses):
    return set([abs(y) for x in clauses for y in x])


def bcp(clauses, unit):
    clausX = []
    for cl in clauses:
        if unit in cl:
            continue
        if -unit in cl:
            new_cl = [x for x in cl if x != -unit]
            if not new_cl:
                return -1
            clausX.append(new_cl)
        else:
            clausX.append(cl)
    return clausX


def pure_literal(clauses):
    literals = set([y for x in clauses for y in x])
    assign = []
    pures = [x for x in literals if -x not in literals]
    for pure in pures:
        clauses = bcp(clauses, pure)
    assign += pures
    return clauses, assign


def unit_propagation(clauses):
    assign = []
    units = [c for c in clauses if len(c) == 1]
    while units:
        unit = (units[0])[0]
        clauses = bcp(clauses, unit)
        assign.append(unit)
        if clauses == -1:
            return -1, []
        if not clauses:
            return clauses, assign
        units = [c for c in clauses if len(c) == 1]
    return clauses, assign


def jeroslow_wang_2_sided(clauses, weight=2):
    aux = {}
    for cl in clauses:
        for lit in cl:
            # Siendo weight=2, len(cl)=3 -> 2^(-3)=0.125
            if abs(lit) in aux:
                aux[abs(lit)] += weight ** -len(cl)
            else:
                aux[abs(lit)] = weight ** -len(cl)
    return aux


def heuristic_selector(clauses):
    # Se devuelve aquel literal que tenga un mayor valor.
    aux = jeroslow_wang_2_sided(clauses)
    return max(aux, key=aux.get)


def dpll(clauses, assign):
    clauses, pure_assignment = pure_literal(clauses)
    clauses, unit_assignment = unit_propagation(clauses)
    assign.extend(pure_assignment + unit_assignment)

    if clauses == - 1:
        return []
    if not clauses:
        return assign

    variable = heuristic_selector(clauses)
    solution = dpll(bcp(clauses, variable), assign + [variable])
    if not solution:
        solution = dpll(bcp(clauses, -variable), assign + [-variable])
    return solution


def solve(clauses):
    literals = getLiterals(clauses)

    res = dpll(clauses, [])
    if res:
        res.extend([x for x in literals if x not in res and -x not in res])
        res.sort(key=lambda x: abs(x))
        return True, dict(zip(literals, [True if x > 0 else False for x in res]))
    else:
        return False, None
