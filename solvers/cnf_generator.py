from utils.helpers import varnum, neighbors, exactly_n

def generate_cnf(grid):
    height = len(grid)
    width = len(grid[0])
    clauses = []

    for r in range(height):
        for c in range(width):
            val = grid[r][c]
            if val.isdigit():
                n = int(val)
                nbs = list(varnum(nr, nc, width) for nr, nc in neighbors(r, c, height, width))
                clauses.extend(exactly_n(nbs, n))

    for r in range(height):
        for c in range(width):
            if grid[r][c].isdigit():
                clauses.append([-varnum(r, c, width)])

    return clauses
