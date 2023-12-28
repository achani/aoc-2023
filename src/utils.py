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
