from utils.helpers import varnum, neighbors

def brute_force(grid):
    height = len(grid)
    width = len(grid[0])
    positions = [(r, c) for r in range(height) for c in range(width) if not grid[r][c].isdigit()]
    n = len(positions)

    for bits in range(2**n):
        assign = {(r, c): ((bits >> i) & 1) == 1 for i, (r, c) in enumerate(positions)}
        valid = True
        for r in range(height):
            for c in range(width):
                if grid[r][c].isdigit():
                    expected = int(grid[r][c])
                    count = sum(
                        assign.get((nr, nc), grid[nr][nc] == 'T')
                        for nr, nc in neighbors(r, c, height, width)
                    )
                    if count != expected:
                        valid = False
                        break
            if not valid:
                break
        if valid:
            model = []
            for r in range(height):
                for c in range(width):
                    v = varnum(r, c, width)
                    if (r, c) in assign:
                        model.append(v if assign[(r, c)] else -v)
                    elif grid[r][c].isdigit():
                        model.append(-v)
            return model
    return None
