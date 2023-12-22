import math
import re


def find_start():
    for i, line in enumerate(lines):
        j = line.find("S")
        if j >= 0:
            return i, j


def at(x, y):
    return grid[x][y]


def towards(direction, pos):
    x, y = pos
    match direction:
        case "N":
            new_x, new_y = x - 1, y
            return (
                (at(new_x, new_y), (new_x, new_y))
                if new_x >= 0
                else ("x", (new_x, new_y))
            )
        case "S":
            new_x, new_y = x + 1, y
            return (
                (at(new_x, new_y), (new_x, new_y))
                if new_x < len(grid)
                else ("x", (new_x, new_y))
            )
        case "E":
            new_x, new_y = x, y + 1
            return (
                (at(new_x, new_y), (new_x, new_y))
                if new_y < len(grid[0])
                else ("x", (new_x, new_y))
            )
        case "W":
            new_x, new_y = x, y - 1
            return (
                (at(new_x, new_y), (new_x, new_y))
                if new_y >= 0
                else ("x", (new_x, new_y))
            )


conn_map = {
    "|": ["N", "S"],
    "7": ["W", "S"],
    "F": ["S", "E"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["W", "N"],
    "N": "7|FS",
    "S": "|LJS",
    "E": "-7JS",
    "W": "-LFS",
}

crossing_pattern_ns = r"(-)|(7L)|(FJ)"
crossing_pattern_ew = r"(|)|(FJ)|(L7)"


def get_next_pos(pos, prev_pos, from_start=False):
    x, y = pos
    current_tile = at(x, y)
    possible_directions = (
        conn_map[current_tile] if not from_start else ["N", "S", "E", "W"]
    )
    for dir in possible_directions:
        next_tile, new_pos = towards(dir, pos)
        if next_tile in conn_map[dir] and prev_pos != new_pos:
            return new_pos, next_tile


def find_loop_length(start):
    x, y = start
    tile_type = at(x, y)
    loop = {start: tile_type}
    current_pos, current_tile = get_next_pos(start, None, from_start=True)
    loop[current_pos] = current_tile
    prev_pos = start
    steps = 1
    while current_pos != start:
        temp = current_pos
        current_pos, current_tile = get_next_pos(current_pos, prev_pos)
        loop[current_pos] = current_tile
        prev_pos = temp
        steps += 1
    return steps, loop


def count_of_loop_crossings(dir, point):
    x, y = point
    match dir:
        case "N":
            str = "".join([grid[x][i] for i in range(x)])
            str = str.replace("|", "")
            return len(re.findall(crossing_pattern_ns, str))
        case "S":
            str = "".join([grid[x][i] for i in range(y, len(grid))])
            str = str.replace("|", "")
            return len(re.findall(crossing_pattern_ns, str))
        case "E":
            str = "".join([grid[i][y] for i in range(x, len(grid[0]))])
            str = str.replace("|", "")
            return len(re.findall(crossing_pattern_ew, str))
        case "W":
            str = "".join([grid[i][y] for i in range(x)])
            str = str.replace("|", "")
            return len(re.findall(crossing_pattern_ew, str))


def calculate_tiles_inside_loop():
    """Logic: In order to be in the loop there should be an odd no. of loop crossings in each direction."""
    count_inside = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in loop:
                continue
            is_inside = True
            for dir in ["N", "S", "E", "W"]:
                if count_of_loop_crossings(dir, (i, j)) % 2 == 0:
                    is_inside = False
                    break
            if is_inside:
                count_inside += 1
                points_in_loop[(i, j)] = at(i, j)
    return count_inside


with open("test2.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()

grid = [[c for c in line] for line in lines]

loop_length, loop = find_loop_length(find_start())
points_in_loop = {}

part2 = calculate_tiles_inside_loop()

for point in points_in_loop:
    for dir in ["N", "S", "E", "W"]:
        crossings = count_of_loop_crossings(dir, point)
        print(f"Point: {point}, Dir: {dir}, Crossings: {crossings}")

print(f"Part 2: {part2}")
print(f"Part 1: {math.ceil(loop_length/2)}")
