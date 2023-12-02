from os import path
input_path = "/Users/ajay/dev/projects/AdventOfCode2023/input/day01.txt"

with open(input_path, 'r') as f:
    lines = f.read().splitlines()
    filtered = map(lambda i: list(filter(lambda x: x.isdigit(), i)), lines)
    ans = sum(list(map(lambda i: int(i[0]) * 10 + int(i[-1]), filtered)))
    print(ans)

