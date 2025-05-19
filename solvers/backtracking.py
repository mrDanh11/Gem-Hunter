# from utils.helpers import varnum, neighbors

# def backtracking(grid):
#     height = len(grid)
#     width = len(grid[0])
#     positions = [(r, c) for r in range(height) for c in range(width) if not grid[r][c].isdigit()]
#     assignment = {}

#     def is_valid():
#         for r in range(height):
#             for c in range(width):
#                 if grid[r][c].isdigit():
#                     expected = int(grid[r][c])
#                     count = sum(
#                         assignment.get((nr, nc), grid[nr][nc] == 'T')
#                         for nr, nc in neighbors(r, c, height, width)
#                     )
#                     if count > expected:
#                         return False
#         return True

#     def backtrack(i):
#         if i == len(positions):
#             return all(
#                 sum(
#                     assignment.get((nr, nc), grid[nr][nc] == 'T')
#                     for nr, nc in neighbors(r, c, height, width)
#                 ) == int(grid[r][c])
#                 for r in range(height) for c in range(width)
#                 if grid[r][c].isdigit()
#             )
#         r, c = positions[i]
#         for val in [True, False]:
#             assignment[(r, c)] = val
#             if is_valid() and backtrack(i + 1):
#                 return True
#             del assignment[(r, c)]
#         return False

#     if backtrack(0):
#         model = []
#         for r in range(height):
#             for c in range(width):
#                 v = varnum(r, c, width)
#                 if (r, c) in assignment:
#                     model.append(v if assignment[(r, c)] else -v)
#                 elif grid[r][c].isdigit():
#                     model.append(-v)
#         return model
#     return None




from utils.helpers import varnum, neighbors

def backtracking(grid):
    height = len(grid)
    width = len(grid[0])
    positions = [(r, c) for r in range(height) for c in range(width) if not grid[r][c].isdigit()]

    # Tính số lượng ô số lân cận để sắp xếp biến ưu tiên (giảm dần)
    def count_constraints(pos):
        r, c = pos
        return sum(1 for nr, nc in neighbors(r, c, height, width) if grid[nr][nc].isdigit())
    positions.sort(key=count_constraints, reverse=True)

    # Lưu số bẫy còn cần đặt ở mỗi ô số
    traps_needed = {}
    for r in range(height):
        for c in range(width):
            if grid[r][c].isdigit():
                traps_needed[(r, c)] = int(grid[r][c])

    assignment = {}

    # Cập nhật trạng thái incremental cho ô số khi gán/thu hồi biến
    def update_traps_needed(r, c, val):
        # val = True nếu ô (r,c) là trap, False nếu là gem
        for nr, nc in neighbors(r, c, height, width):
            if (nr, nc) in traps_needed:
                if val:
                    traps_needed[(nr, nc)] -= 1
                else:
                    traps_needed[(nr, nc)] += 1

    def is_valid(r, c, val):
        # Kiểm tra ngay ô số lân cận xem còn khả thi không
        for nr, nc in neighbors(r, c, height, width):
            if (nr, nc) in traps_needed:
                needed = traps_needed[(nr, nc)]
                if needed < 0 or needed > len([
                    (x, y) for x, y in neighbors(nr, nc, height, width)
                    if (x, y) not in assignment
                ]):
                    # Cần nhiều bẫy hơn số ô trống còn lại hoặc đã dư bẫy
                    return False
        return True

    def backtrack(i=0):
        if i == len(positions):
            # Kiểm tra tất cả ô số đã thoả mãn đủ bẫy
            return all(v == 0 for v in traps_needed.values())

        r, c = positions[i]
        for val in [True, False]:
            assignment[(r, c)] = val
            update_traps_needed(r, c, val)
            if is_valid(r, c, val):
                if backtrack(i + 1):
                    return True
            update_traps_needed(r, c, not val)  # Thu hồi thay đổi
            del assignment[(r, c)]
        return False

    if backtrack():
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
