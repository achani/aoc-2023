"""Solution for Advent of Code 2023 day 14"""


def score(grid):
    score = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "O":
                score += len(grid) - r
    return score


def spin(grid):
    for dir in ["N", "W", "S", "E"]:
        grid = move(grid, dir)
    return grid


def print_grid(grid):
    for row in grid:
        print("".join(row))


def move(grid, dir):
    R, C = len(grid), len(grid[0])
    new_grid = [["." for _ in range(C)] for _ in range(R)]

    match dir:
        case "N" | "S":
            (step, start, stop) = (1, 0, R) if dir == "N" else (-1, R - 1, -1)
            for i in range(C):
                col = [row[i] for row in grid]
                moves = 0
                for j in range(start, stop, step):
                    if col[j] == "#":
                        new_grid[j][i] = "#"
                        moves = 0
                    if col[j] == ".":
                        moves += 1
                    if col[j] == "O":
                        new_grid[j - step * moves][i] = "O"
        case "E" | "W":
            (step, start, stop) = (1, 0, C) if dir == "W" else (-1, C - 1, -1)
            for i in range(R):
                row = grid[i]
                moves = 0
                for j in range(start, stop, step):
                    if row[j] == "#":
                        new_grid[i][j] = "#"
                        moves = 0
                    if row[j] == ".":
                        moves += 1
                    if row[j] == "O":
                        new_grid[i][j - step * moves] = "O"
    return new_grid


def spin_and_get_score(cycles, grid):
    HISTORY = {}
    total_cycles = cycles
    cycles_completed = 0

    while cycles_completed < total_cycles:
        grid = spin(grid)
        #print(f"Cycles Completed: {cycles_completed}, score: {score(grid)}")
        cycles_completed += 1
        hash = tuple(tuple(v for v in row) for row in grid)
        if hash in HISTORY:
            last_seen = HISTORY[hash]
            #print(f"Found in history. {cycles_completed} = {last_seen}")
            freq = cycles_completed - last_seen
            cycles_to_go = total_cycles - cycles_completed
            cycles_completed += freq * (cycles_to_go // freq)
        HISTORY[hash] = cycles_completed
    return score(grid)


with open("input.txt", "r") as f:
    lines = f.read().splitlines()


grid = [[c for c in row] for row in lines]


print(f"Part 1: {score(move(grid,'N'))}")
print(f"Part 2: {spin_and_get_score(1000000000, grid)}")