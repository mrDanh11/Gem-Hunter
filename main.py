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
#         print("0. Thoát")
#         choice = input("Nhập số (0-3): ").strip()

#         if choice not in {"1", "2", "3", "0"}:
#             print("❌ Lựa chọn không hợp lệ.")
#             continue
#         if choice == "0":
#             print("👋 Tạm biệt!")
#             break

#         input_file = f"testcases/testcase{choice}.txt"
#         if not os.path.exists(input_file):
#             print("❌ File input không tồn tại.")
#             continue

#         with open(input_file, 'r') as f:
#             grid_lines = [line.strip() for line in f if line.strip()]
#         grid = parse_input(grid_lines)

#         print("\nChọn thuật toán:")
#         print("1. PySAT (Nhanh, chính xác)")
#         print("2. Brute-force (Chậm, kiểm chứng)")
#         print("3. Backtracking (Trung bình)")
#         algo = input("Thuật toán? (1-3): ").strip()

#         algo_map = {"1": "pysat", "2": "brute", "3": "backtrack"}
#         method = algo_map.get(algo)
#         if not method:
#             print("❌ Thuật toán không hợp lệ.")
#             continue

#         model = solve(grid, method)
#         if model:
#             res = print_solution(grid, model)
#             print("\n✅ Kết quả:")
#             for row in res:
#                 print(', '.join(row))
#             base_name = f"{method}_testcase{choice}"
#             filename = get_unique_output_filename("output", base_name)
#             with open(filename, 'w') as f:
#                 for row in res:
#                     f.write(', '.join(row) + '\n')
#             print(f"\n💾 Đã lưu vào {filename}")
#         else:
#             print("❌ Không tìm được lời giải.")

# if __name__ == "__main__":
#     run_solver_with_choice()



from cli.menu import run_solver_with_choice

if __name__ == "__main__":
    run_solver_with_choice()



