import itertools

def varnum(r, c, width):
    return r * width + c + 1

def parse_input(grid_lines):
    grid = []
    for line in grid_lines:
        row = [x.strip() for x in line.strip().split(',')]
        grid.append(row)
    return grid

def neighbors(r, c, height, width):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                yield nr, nc

def exactly_n(vars_, n):
    clauses = []
    length = len(vars_)
    for comb in itertools.combinations(vars_, length - n + 1):
        clauses.append(list(comb))
    for comb in itertools.combinations(vars_, n + 1):
        clauses.append([-v for v in comb])
    return clauses
