from utils.helpers import varnum, neighbors, exactly_n

def generate_cnf(grid):
    height = len(grid)
    width = len(grid[0])
    clauses = []

     # duyệt từng ô trong lưới
    for r in range(height):
        for c in range(width):
            val = grid[r][c]
            if val.isdigit():
                n = int(val)
                # lấy danh sách các biến logic của ô lân cận (neighbor),
                # mỗi biến ứng với ô đó theo hàm varnum (biến logic dạng số nguyên)
                nbs = list(varnum(nr, nc, width) for nr, nc in neighbors(r, c, height, width))
                # sinh các clause CNF thể hiện ràng buộc "chính xác n trong số các ô lân cận là bẫy"
                # exactly_n trả về danh sách các clause
                clauses.extend(exactly_n(nbs, n))

    # các ô có số KHÔNG thể là bẫy
    # (vì ô số chỉ dùng để biểu thị số bẫy xung quanh, không thể chứa bẫy)
    for r in range(height):
        for c in range(width):
            if grid[r][c].isdigit():
                # thêm clause biểu diễn: biến này phải là False (không phải bẫy)
                clauses.append([-varnum(r, c, width)])

    return clauses
