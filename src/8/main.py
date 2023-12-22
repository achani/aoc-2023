from math import lcm


def traverse_path(start, there_yet):
    steps = cursor = 0
    curr_location = start
    while not there_yet(curr_location):
        curr_location = map[curr_location][int(path[cursor])]
        steps += 1
        cursor += 1
        cursor = 0 if cursor == len(path) else cursor
    return steps


def traverse_path_part2():
    starting_nodes = [node for node in map.keys() if node[-1] == "A"]
    step_counts = [
        traverse_path(node, lambda x: x[-1] == "Z") for node in starting_nodes
    ]
    return lcm(*step_counts)


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read()

path, map_raw = lines.split("\n\n")
path = path.replace("L", "0").replace("R", "1")

map_raw = list(map(lambda x: x.replace("(", "").replace(")", ""), map_raw.split("\n")))

map = {
    key: value
    for key, value in list(
        map(
            lambda x: (x[0], x[1].split(", ")),
            list(map(lambda x: x.split(" = "), map_raw)),
        )
    )
}

part1 = traverse_path("AAA", lambda x: x == "ZZZ")
part2 = traverse_path_part2()

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
