from utils.helpers import varnum, neighbors

def backtracking(grid):
    height = len(grid)
    width = len(grid[0])
    positions = [(r, c) for r in range(height) for c in range(width) if not grid[r][c].isdigit()]
    assignment = {}

    def is_valid():
        for r in range(height):
            for c in range(width):
                if grid[r][c].isdigit():
                    expected = int(grid[r][c])
                    count = sum(
                        assignment.get((nr, nc), grid[nr][nc] == 'T')
                        for nr, nc in neighbors(r, c, height, width)
                    )
                    if count > expected:
                        return False
        return True

    def backtrack(i):
        if i == len(positions):
            return all(
                sum(
                    assignment.get((nr, nc), grid[nr][nc] == 'T')
                    for nr, nc in neighbors(r, c, height, width)
                ) == int(grid[r][c])
                for r in range(height) for c in range(width)
                if grid[r][c].isdigit()
            )
        r, c = positions[i]
        for val in [True, False]:
            assignment[(r, c)] = val
            if is_valid() and backtrack(i + 1):
                return True
            del assignment[(r, c)]
        return False

    if backtrack(0):
        model = []
        for r in range(height):
            for c in range(width):
                v = varnum(r, c, width)
                if (r, c) in assignment:
                    model.append(v if assignment[(r, c)] else -v)
                elif grid[r][c].isdigit():
                    model.append(-v)
        return model
    return None
