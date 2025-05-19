# import os
# import time
# from utils.helpers import parse_input, varnum
# from solvers.cnf_generator import generate_cnf
# from solvers.pysat_solver import solve_with_pysat
# from solvers.brute_force import brute_force
# from solvers.backtracking import backtracking

# def print_solution(grid, model):
#     height = len(grid)
#     width = len(grid[0])
#     var_map = {abs(v): v > 0 for v in model}
#     result = []
#     for r in range(height):
#         row = []
#         for c in range(width):
#             val = grid[r][c]
#             v = varnum(r, c, width)
#             if val.isdigit():
#                 row.append(val)
#             else:
#                 row.append('T' if var_map.get(v, False) else 'G')
#         result.append(row)
#     return result

# def solve(grid, method: str):
#     clauses = generate_cnf(grid)
#     start = time.time()

#     if method == "pysat":
#         model = solve_with_pysat(clauses)
#     elif method == "brute":
#         model = brute_force(grid)
#     elif method == "backtrack":
#         model = backtracking(grid)
#     else:
#         print("Unknown method.")
#         return None

#     print(f"[{method.upper()}] Time: {time.time() - start:.6f}s")
#     return model

# def get_unique_output_filename(folder, base_name):
#     filename = f"{base_name}.txt"
#     counter = 1
#     while os.path.exists(os.path.join(folder, filename)):
#         counter += 1
#         filename = f"{base_name}_{counter}.txt"
#     return os.path.join(folder, filename)

# def run_solver_with_choice():
#     print("=== GEM HUNTER SOLVER ===")
#     os.makedirs("output", exist_ok=True)

#     while True:
#         print("\nChọn test case:")
#         print("1. Testcase 1")
#         print("2. Testcase 2")
#         print("3. Testcase 3")
#         print("0. Exit")
#         choice = input("Choose number(0-3): ").strip()

#         if choice not in {"1", "2", "3", "0"}:
#             print("Invalid Selection!!")
#             continue
#         if choice == "0":
#             print("Exiting..")
#             break

#         input_file = f"testcases/testcase{choice}.txt"
#         if not os.path.exists(input_file):
#             print("Invalid file input!!")
#             continue

#         with open(input_file, 'r') as f:
#             grid_lines = [line.strip() for line in f if line.strip()]
#         grid = parse_input(grid_lines)

#         print("\nChoose algorithms:")
#         print("1. Pysat ")
#         print("2. Brute-force ")
#         print("3. Backtracking ")
#         algo = input("Algorithms? (1-3): ").strip()

#         algo_map = {"1": "pysat", "2": "brute", "3": "backtrack"}
#         method = algo_map.get(algo)
#         if not method:
#             print("Invalid algorithms!!")
#             continue

#         model = solve(grid, method)
#         if model:
#             res = print_solution(grid, model)
#             print("\nResult:")
#             for row in res:
#                 print(', '.join(row))
#             base_name = f"{method}_testcase{choice}"
#             filename = get_unique_output_filename("output", base_name)
#             with open(filename, 'w') as f:
#                 for row in res:
#                     f.write(', '.join(row) + '\n')
#             print(f"\nSaved to {filename}")
#         else:
#             print("No solution found!!")



import os
import time
from utils.helpers import parse_input, varnum
from solvers.cnf_generator import generate_cnf
from solvers.pysat_solver import solve_with_pysat
from solvers.brute_force import brute_force
from solvers.backtracking import backtracking

def print_solution(grid, model):
    height = len(grid)
    width = len(grid[0])
    var_map = {abs(v): v > 0 for v in model}
    result = []
    for r in range(height):
        row = []
        for c in range(width):
            val = grid[r][c]
            v = varnum(r, c, width)
            if val.isdigit():
                row.append(val)
            else:
                row.append('T' if var_map.get(v, False) else 'G')
        result.append(row)
    return result

def solve(grid, method: str):
    clauses = generate_cnf(grid)
    start = time.time()

    if method == "pysat":
        model = solve_with_pysat(clauses)
    elif method == "brute":
        model = brute_force(grid)
    elif method == "backtrack":
        model = backtracking(grid)
    else:
        print("Unknown method.")
        return None

    print(f"[{method.upper()}] Time: {time.time() - start:.6f}s")
    return model

def run_solver_with_choice():
    print("=== GEM HUNTER SOLVER ===")
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    while True:
        print("\nSelect Test Case:")
        print("1. input_1.txt")
        print("2. input_2.txt")
        print("3. input_3.txt")
        print("0. Exit")
        choice = input("Choose (0-3): ").strip()

        if choice not in {"1", "2", "3", "0"}:
            print("Invalid Selection.")
            continue
        if choice == "0":
            print("Exiting.")
            break

        input_file = f"input/input_{choice}.txt"
        output_file = f"output/output_{choice}.txt"

        if not os.path.exists(input_file):
            print("Input file not found!")
            continue

        with open(input_file, 'r') as f:
            grid_lines = [line.strip() for line in f if line.strip()]
        grid = parse_input(grid_lines)

        print("\nSelect Algorithm:")
        print("1. PySAT")
        print("2. Brute-force")
        print("3. Backtracking")
        algo = input("Algorithm (1-3): ").strip()

        algo_map = {"1": "pysat", "2": "brute", "3": "backtrack"}
        method = algo_map.get(algo)
        if not method:
            print("Invalid algorithm.")
            continue

        model = solve(grid, method)
        if model:
            res = print_solution(grid, model)
            print("\nResult:")
            for row in res:
                print(', '.join(row))
            with open(output_file, 'w') as f:
                for row in res:
                    f.write(', '.join(row) + '\n')
            print(f"\nSaved to {output_file}")
        # else:
        #     print("No solution found.")
