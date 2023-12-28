from collections import defaultdict


offsets = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


points = [(0, 0)]
for line in lines:
    d, steps, color = line.split()
    steps = int(steps)
    last_point = points[-1]
    points.add((last_point[0] + offsets[d][0], last_point[1] + offsets[d][1]))


print(ans)
