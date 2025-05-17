from pysat.solvers import Glucose3

def solve_with_pysat(clauses):
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)
    return solver.get_model() if solver.solve() else None
