class Grid:
    def __init__(self, pattern) -> None:
        self.grid = [[c for c in row] for row in pattern.split("\n")]

    def col(self, c):
        return [self.grid[r][c] for r, _ in enumerate(self.grid)]

    def row(self, r):
        return self.grid[r]

    def row_count(self):
        return len(self.grid)

    def col_count(self):
        return len(self.grid[0])


def check_col_symmetry(grid: Grid, allowed_errors=0):
    for i in range(grid.col_count() - 1):
        errors = 0
        for j in range(grid.col_count()):
            l, r = i - j, i + 1 + j
            if 0 <= l < r < grid.col_count():
                errors += len(
                    [a for a, v in enumerate(grid.col(l)) if v != grid.col(r)[a]]
                )
        if errors == allowed_errors:
            return i + 1
    return 0


def check_row_symmetry(grid: Grid, allowed_errors=0):
    for i in range(grid.row_count() - 1):
        errors = 0
        for j in range(grid.row_count()):
            l, r = i - j, i + 1 + j
            if 0 <= l < r < grid.row_count():
                errors += len(
                    [a for a, v in enumerate(grid.row(l)) if v != grid.row(r)[a]]
                )
        if errors == allowed_errors:
            return i + 1
    return 0


def solve(allowed_errors=0):
    ans = 0
    for pattern in patterns:
        grid = Grid(pattern)
        cols = check_col_symmetry(grid, allowed_errors)
        ans += cols
        rows = check_row_symmetry(grid, allowed_errors)
        ans += 100 * rows
    return ans


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read()

patterns = lines.split("\n\n")

print(f"Part 1: {solve()}")
print(f"Part 2: {solve(1)}")
