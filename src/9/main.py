from collections import Counter


def get_prediction_future(values):
    if Counter(values).most_common()[0][1] == len(values):
        return values[-1]
    else:
        return values[-1] + get_prediction_future(
            [(values[i + 1] - values[i]) for i in range(len(values) - 1)]
        )


def get_prediction_past(values):
    if Counter(values).most_common()[0][1] == len(values):
        return values[0]
    else:
        return values[0] - get_prediction_past(
            [(values[i + 1] - values[i]) for i in range(len(values) - 1)]
        )


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()


values = list(map(lambda x: [int(i) for i in x.split()], lines))

part1 = sum(list(map(lambda x: get_prediction_future(x), values)))
part2 = sum(list(map(lambda x: get_prediction_past(x), values)))

print(f"Part 1: {part1} \nPart 2: {part2}")
