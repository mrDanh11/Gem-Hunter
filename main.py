from pysat.solvers import Glucose3
import time
import itertools

# Biến logic: mỗi ô (r,c) sẽ được map thành số nguyên (variable) = r * width + c + 1

def varnum(r, c, width):
    return r * width + c + 1

def parse_input(grid_lines):
    grid = []
    for line in grid_lines:
        # phân tách theo dấu phẩy và loại bỏ khoảng trắng
        row = [x.strip() for x in line.strip().split(',')]
        grid.append(row)
    return grid

def neighbors(r, c, height, width):
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r+dr, c+dc
            if 0 <= nr < height and 0 <= nc < width:
                yield nr, nc

# Sinh ràng buộc CNF rằng trong các ô lân cận có đúng N bẫy
# Cách làm: Với danh sách các biến (lân cận), tạo ràng buộc tổng số biến True = N
# Cách viết CNF cho tổng đúng bằng N phức tạp, nên ta dùng cách biểu diễn tổng (cardinality constraint) đơn giản qua tổ hợp

def exactly_n(vars_, n):
    # Ràng buộc đúng n biến trong vars_ là True:
    # 1) ít nhất n: tổ hợp tất cả các tổ hợp vars_ chọn (len(vars_)-n+1) biến phủ (OR)
    # 2) tối đa n: loại bỏ các tổ hợp vars_ chọn (n+1) biến True cùng lúc (NOT)

    # Cách đơn giản dùng quy tắc:
    # Ít nhất n: Tổ hợp len(vars_)-n+1 biến phải có ít nhất một True
    # Tối đa n: Tổ hợp (n+1) biến không được đồng thời True

    clauses = []

    length = len(vars_)
    # Ít nhất n
    for comb in itertools.combinations(vars_, length - n + 1):
        clauses.append(list(comb))  # OR các biến

    # Tối đa n
    for comb in itertools.combinations(vars_, n + 1):
        clauses.append([-v for v in comb])  # không thể tất cả cùng True

    return clauses

def generate_cnf(grid):
    height = len(grid)
    width = len(grid[0])
    clauses = []

    for r in range(height):
        for c in range(width):
            val = grid[r][c]
            if val.isdigit():
                n = int(val)
                nbs = list(varnum(nr,nc,width) for nr,nc in neighbors(r,c,height,width))
                # Gán ràng buộc đúng n trong số các ô lân cận là trap (True)
                clauses.extend(exactly_n(nbs, n))
            # Nếu ô là số hoặc trap/gem thì ta không gán biến gì cho ô đó
            # Nhưng cần thêm ràng buộc:
            # - Nếu ô là số => ô đó không phải trap
            # - Nếu ô trống => không biết

    # Thêm ràng buộc ô có số không thể là trap
    for r in range(height):
        for c in range(width):
            val = grid[r][c]
            if val.isdigit():
                v = varnum(r,c,width)
                # Ô có số phải là False (không phải trap)
                clauses.append([-v])

    return clauses

def print_solution(grid, model):
    height = len(grid)
    width = len(grid[0])
    var_map = {}
    for v in model:
        if v > 0:
            var_map[v] = True
        else:
            var_map[-v] = False
    res = []
    for r in range(height):
        row = []
        for c in range(width):
            val = grid[r][c]
            v = varnum(r,c,width)
            if val.isdigit():
                # Giữ nguyên số
                row.append(val)
            else:
                if v in var_map:
                    if var_map[v]:
                        row.append('T')  # trap
                    else:
                        row.append('G')  # gem
                else:
                    # Không xác định, giữ nguyên dấu _
                    row.append(val)
        res.append(row)
    return res

# Thuật toán brute-force đơn giản thử tất cả cấu hình hợp lệ
def brute_force(grid):
    height = len(grid)
    width = len(grid[0])
    positions = []
    for r in range(height):
        for c in range(width):
            if not grid[r][c].isdigit():
                positions.append((r,c))
    n = len(positions)
    # Duyệt tất cả các khả năng (0=gem, 1=trap)
    for bits in range(2**n):
        assign = {}
        for i, (r,c) in enumerate(positions):
            assign[(r,c)] = (bits >> i) & 1 == 1

        # Kiểm tra tính hợp lệ với các ô số
        valid = True
        for r in range(height):
            for c in range(width):
                if grid[r][c].isdigit():
                    expected = int(grid[r][c])
                    count_traps = 0
                    for nr,nc in neighbors(r,c,height,width):
                        if (nr,nc) in assign:
                            if assign[(nr,nc)]:
                                count_traps += 1
                        else:
                            # Nếu là số hoặc trap thì coi như không phải trap
                            if grid[nr][nc] == 'T':
                                count_traps += 1
                    if count_traps != expected:
                        valid = False
                        break
            if not valid:
                break
        if valid:
            # Tạo model dạng danh sách số biến, True biến dương, False âm
            model = []
            for r in range(height):
                for c in range(width):
                    v = varnum(r,c,width)
                    if (r,c) in assign:
                        if assign[(r,c)]:
                            model.append(v)
                        else:
                            model.append(-v)
                    else:
                        # Ô số: luôn False
                        if grid[r][c].isdigit():
                            model.append(-v)
            return model
    return None

def backtracking(grid):
    height = len(grid)
    width = len(grid[0])
    positions = [(r,c) for r in range(height) for c in range(width) if not grid[r][c].isdigit()]
    assignment = {}

    def is_valid():
        for r in range(height):
            for c in range(width):
                if grid[r][c].isdigit():
                    expected = int(grid[r][c])
                    count_traps = 0
                    for nr, nc in neighbors(r,c,height,width):
                        if (nr,nc) in assignment and assignment[(nr,nc)]:
                            count_traps += 1
                        elif grid[nr][nc] == 'T':
                            count_traps += 1
                    if count_traps > expected:
                        return False
        return True

    def backtrack(i):
        if i == len(positions):
            # Kiểm tra chính xác bằng
            for r in range(height):
                for c in range(width):
                    if grid[r][c].isdigit():
                        expected = int(grid[r][c])
                        count_traps = 0
                        for nr, nc in neighbors(r,c,height,width):
                            if (nr,nc) in assignment and assignment[(nr,nc)]:
                                count_traps += 1
                            elif grid[nr][nc] == 'T':
                                count_traps += 1
                        if count_traps != expected:
                            return False
            return True

        r, c = positions[i]
        for val in [True, False]:
            assignment[(r,c)] = val
            if is_valid():
                if backtrack(i+1):
                    return True
            del assignment[(r,c)]
        return False

    if backtrack(0):
        model = []
        for r in range(height):
            for c in range(width):
                v = varnum(r, c, width)
                if (r,c) in assignment:
                    if assignment[(r,c)]:
                        model.append(v)
                    else:
                        model.append(-v)
                else:
                    if grid[r][c].isdigit():
                        model.append(-v)
        return model
    else:
        return None


# Hàm chạy tổng hợp
def run_solver(grid_lines):
    grid = parse_input(grid_lines)
    height = len(grid)
    width = len(grid[0])

    print("Input grid:")
    for row in grid:
        print(', '.join(row))

    # Sinh CNF
    clauses = generate_cnf(grid)

    # Giải bằng pysat
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    start = time.time()
    sat = solver.solve()
    end = time.time()

    if sat:
        model = solver.get_model()
        print("\nSolution found by pysat (Glucose3) in %.6f seconds:" % (end - start))
        res = print_solution(grid, model)
        for row in res:
            print(', '.join(row))
    else:
        print("No solution found by pysat solver")

    # Giải bằng brute-force
    print("\nSolving by brute-force:")
    start = time.time()
    model = brute_force(grid)
    end = time.time()
    if model:
        print("Solution found by brute-force in %.6f seconds:" % (end - start))
        res = print_solution(grid, model)
        for row in res:
            print(', '.join(row))
    else:
        print("No solution found by brute-force")

    # Giải bằng backtracking
    print("\nSolving by backtracking:")
    start = time.time()
    model = backtracking(grid)
    end = time.time()
    if model:
        print("Solution found by backtracking in %.6f seconds:" % (end - start))
        res = print_solution(grid, model)
        for row in res:
            print(', '.join(row))
    else:
        print("No solution found by backtracking")

if __name__ == "__main__":
    # Ví dụ input nhỏ 3x4 (dùng dấu _ cho ô trống)
    # 5x5
    # input_example = [
    #     "_, 3, _, _, 2",
    #     "_, 4, _, _, _",
    #     "_, _, 3, _, 3",
    #     "2, _, _, _, _",
    #     "_, 1, _, 3, _",
    # ]

    # 11x11
    # input_example = [
    #     "_, _, _, 2, _, _, _, 1, _, _",
    #     "_, 3, _, _, _, 2, _, _, 3, _",
    #     "_, _, 2, _, _, _, _, 2, _, _",
    #     "2, _, _, 3, _, _, 2, _, _, 2",
    #     "_, _, _, _, 2, _, _, _, 3, _",
    #     "_, 3, _, _, _, 2, _, _, _, 2",
    #     "_, _, _, 1, _, _, _, 3, _, _",
    #     "3, _, _, _, 2, _, _, _, _, 3",
    #     "_, _, 3, _, _, _, 2, _, _, _",
    #     "_, 2, _, _, _, 3, _, _, 2, _"
    # ]
    # input_example = [
    #     "_, _, 2, _, _, _, 3, _, _, _, 2, _, _, 1, _, _, _, 2, _, _",
    #     "_, 3, _, _, 2, _, _, _, _, 3, _, _, _, _, 2, _, _, _, _, 2",
    #     "_, _, _, 2, _, _, _, 3, _, _, _, 2, _, _, _, _, _, 2, _, _"
    #     "2, _, _, _, _, 3, _, _, _, 2, _, _, 2, _, _, _, 3, _, _, _",
    #     "_, _, 2, _, _, _, _, 2, _, _, _, _, 3, _, _, 2, _, _, 3, _",
    #     "_, _, _, 3, _, _, _, _, 2, _, _, _, _, 2, _, _, _, 3, _, _"
    #     "_, 2, _, _, _, 2, _, _, _, 3, _, _, _, _, _, 3, _, _, _, _",
    #     "3, _, _, _, _, _, _, 2, _, _, _, 3, _, _, _, _, _, 2, _, _",
    #     "_, _, 3, _, _, 2, _, _, _, _, _, _, 2, _, _, 2, _, _, 3, _",
    #     "_, _, _, 2, _, _, _, 3, _, _, _, _, _, 3, _, _, _, 2, _, _",
    #     "2, _, _, _, _, 3, _, _, 2, _, _, _, 2, _, _, _, _, _, _, 2",
    #     "_, 3, _, _, _, _, 2, _, _, _, 3, _, _, _, _, _, 3, _, _, _",
    #     "_, _, _, 3, _, _, _, _, _, 2, _, _, _, _, 2, _, _, _, 2, _",
    #     "_, 2, _, _, _, 2, _, _, _, _, _, _, 3, _, _, _, _, _, _, _",
    #     "3, _, _, _, _, _, _, 2, _, 2, _, _, _, 2, _, _, _, 3, _, _",
    #     "_, _, 3, _, _, _, _, 3, _, _, _, 2, _, _, _, 2, _, _, _, _",
    #     "_, _, _, 2, _, _, _, _, 2, _, _, _, _, 3, _, _, _, _, 3, _",
    #     "_, 2, _, _, _, 3, _, _, _, _, _, _, 2, _, _, 2, _, _, _, _",
    #     "_, _, _, 4, _, _, _, _, _, 2, _, _, _, _, 3, _, _, _, _, _",
    #     "_, 2, _, _, _, 2, _, 3, _, _, _, 2, _, _, _, _, _, _, 3, _"
    # ]
    input_example = [
        "_, _, _, _, _, _, _, 2, _, 2, _, 1, 1, _, _, _, 1, 2, 2, 1",
        "_, 1, 1, 1, _, _, _, 2, _, 2, 1, _, 1, _, _, _, 1, _, _, 1",
        "_, 1, _, 1, _, 1, 1, 2, 1, 1, 2, 2, 2, _, _, 1, 3, 4, 3, 1",
        "_, 1, 1, 1, _, 1, _, 2, 1, 2, 3, _, _, _, _, 1, _, _, 1, _",
        "1, 1, _, 1, 1, 2, 1, 2, _, 3, _, _, _, 1, 1, 2, 2, 2, 1, _",
        "_, 2, 2, 3, _, 3, 1, 1, 1, _, _, 4, 3, 4, _, 3, 1, 1, _, _",
        "2, _, 2, _, _, _, 2, 1, 1, 1, 1, 2, _, _, _, _, _, 1, _, _",
        "_, 1, 2, 2, 4, _, 4, _, 2, _, _, 1, 3, 4, _, _, 4, 3, 1, _",
        "1, 1, 1, 1, 2, _, 4, _, 3, _, _, 1, 2, _, _, 3, _, _, 2, 1",
        "2, _, 2, 1, _, 2, 3, _, 3, 1, _, 1, _, 3, 2, 2, _, 5, _, 2",
        "3, _, 3, 2, 2, 1, 2, _, _, 1, _, 2, 3, _, 1, 1, 1, 3, _, _",
       " _, 4, 3, _, 2, 1, 1, _, 2, 2, 3, _, 3, _, 1, _, _, 2, 3, 3",
        "_, _, 3, 3, _, 1, 1, 2, 2, 2, _, _, 2, _, _, 1, 1, 2, _, _",
        "_, 2, 2, _, 2, 1, 1, 2, _, 2, _, 3, 2, _, _, 1, _, 2, 2, 2",
        "_, _, _, 3, 4, 2, _, _, 2, 1, 2, _, 3, 1, _, 1, 2, 3, 3, 2",
        "1, 1, 2, _, _, _, 3, 1, 2, 1, 3, _, _, 1, _, 1, 2, _, _, _",
        "1, _, 3, 4, 6, _, 3, _, 1, _, 2, 2, 2, 1, _, 1, _, 3, 3, 2",
        "1, 2, _, _, _, _, 2, _, _, 1, 2, 1, 1, _, _, 1, 1, 1, _, _",
        "1, 2, 2, _, 2, 2, 1, _, _, _, 1, _, 2, 1, _, 1, 2, 3, _, 1",
        "1, _, 1, _, _, _, _, _, _, _, _, 2, _, 1, _, 1, _, _, _, 1"
    ]

    run_solver(input_example)
