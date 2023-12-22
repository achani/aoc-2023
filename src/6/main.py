"""Solution for Advent of Code 2023 Day 6"""

import math
from functools import reduce


def find_solution(t, max_distance):
    """Solve the inequality -x^2 + tx - max_distance > 0"""
    a = float(-1)
    b = float(t)
    c = float(-1 * max_distance)
    discriminant = math.sqrt(b * b - 4 * a * c)

    root1 = (-1 * b + discriminant) / (2.0 * a)
    root2 = (-1 * b - discriminant) / (2.0 * a)
    solution = (math.ceil(root2) - math.floor(root1)) - 1
    return solution


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()
    for line in lines:
        if "Time:" in line:
            times = [int(x) for x in line.split(":")[1].split()]
            time_2 = int("".join(line.split(":")[1].split()))
        if "Distance:" in line:
            distances = [int(x) for x in line.split(":")[1].split()]
            distance_2 = int("".join(line.split(":")[1].split()))

races = zip(times, distances)
part1 = reduce(lambda x, y: x * y, [find_solution(race[0], race[1]) for race in races])
part2 = find_solution(time_2, distance_2)
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
