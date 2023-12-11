from itertools import combinations


def get_sum(spacing):
    sum_ = 0
    for c in galaxy_comb: 
        r1,r2,c1,c2 = c[0][0], c[1][0], c[0][1], c[1][1]
        empty_rows_between = len([row for row in empty_rows if min(r1,r2) < row < max(r1,r2)])
        empty_cols_between = len([col for col in empty_columns if (min(c1,c2) < col < max(c1,c2))])
        sum_ += abs(r2-r1) + (empty_cols_between * (spacing-1))\
            + abs(c2-c1) + (empty_rows_between * (spacing-1))
    return sum_


with open("input.txt", 'r', encoding="UTF8") as f:
    lines = f.read().splitlines()

grid = [[c for c in line] for line in lines]
empty_rows = [i for i,r in enumerate(grid) if "#" not in r]
empty_columns = [i for i, _ in enumerate(grid[0]) if "#" not in [grid[x][i] for x, _ in enumerate(grid)]]
galaxy_locations = [(i,j) for i,r in enumerate(grid) for j,c in enumerate(r) if c == "#"]
galaxy_comb = list(combinations(galaxy_locations,2))

print(f"Part 1: {get_sum(2)}")
print(f"Part 2: {get_sum(1000000)}")