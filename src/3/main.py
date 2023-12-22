import re

pattern_no = r"\d+"
pattern_symbol = r"[^\d\.]"
pattern_star = r"\*"


def scan_line_part1(line, prv, nxt):
    ans = 0
    for match in re.finditer(pattern_no, line):
        start, stop = match.span()
        begin = start - 1 if start > 0 else start
        end = stop + 1 if stop < len(line) else stop
        is_part_no = False
        if (prv and re.search(pattern_symbol, prv[begin:end])) or (nxt and re.search(pattern_symbol, nxt[begin:end])):
            is_part_no = True
        if begin > 0 and re.search(pattern_symbol, line[begin : begin + 1]):
            is_part_no = True
        if stop < len(line) and re.search(pattern_symbol, line[stop : stop + 1]):
            is_part_no = True
        ans += int(match.group()) if is_part_no else 0
    return ans


def scan_line_part2(line, prv, nxt, line_no):
    star_connections = []
    for match in re.finditer(pattern_no, line):
        start, stop = match.span()
        begin = start - 1 if start > 0 else start
        end = stop + 1 if stop < len(line) else stop
        # is there a star on the left?
        if start > 0 and line[begin] == "*":
            star_connections.append((str(line_no) + ":" + str(begin), match.group()))
        # is there a star on the right?
        if stop < len(line) and line[stop] == "*":
            star_connections.append((str(line_no) + ":" + str(stop), match.group()))
        if prv:
            for i in range(end - begin):
                if prv[i + begin] == "*":
                    star_connections.append((str(line_no - 1) + ":" + str(i + begin), match.group()))
        if nxt:
            for i in range(end - begin):
                if nxt[i + begin] == "*":
                    star_connections.append((str(line_no + 1) + ":" + str(i + begin), match.group()))
    return star_connections


def solve_part1(lines):
    ans = 0
    prev = None
    for line_no in range(len(lines)):
        ans += scan_line_part1(lines[line_no],prev,lines[line_no + 1] if line_no < len(lines) - 1 else None)
        prev = lines[line_no]
    return ans


def solve_part2(lines):
    prev = None
    connections = {}
    for line_no in range(len(lines)):
        conn_line = scan_line_part2(lines[line_no],prev,lines[line_no + 1] if line_no < len(lines) - 1 else None, line_no)
        for conn in conn_line: 
            connected_numbers = connections.get(conn[0], [])
            connected_numbers.append(conn[1])
            connections[conn[0]] = connected_numbers
        prev = lines[line_no]
    return sum([int(v[0]) * int(v[1]) for v in connections.values() if len(v) == 2])


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

print(f"Part 1: {solve_part1(lines)}")
print(f"Part 2: {solve_part2(lines)}")

