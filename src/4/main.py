"""Solution to Advent of Code 2023 Day4"""


def get_match_count(card):
    """Get the no of winning numbers on the card"""
    left, right = card.split("|")
    winning = [int(i) for i in left.split(":")[1].split()]
    card_nos = [int(i) for i in right.split()]
    return len(list(set(winning) & set(card_nos)))


def solve_part1():
    """Solution for Part 1"""
    ans = 0
    for line in lines:
        match_count = get_match_count(line)
        if match_count > 0:
            ans += 2 ** (match_count - 1)
    print("Part 1: " + str(ans))


def solve_part2():
    """Solution for Part 2"""
    ans = 0
    card_counts = [1] * len(lines)

    for i, card in enumerate(lines):
        match_count = get_match_count(card)
        for j in range(match_count):
            card_counts[i + 1 + j] += card_counts[i]
    ans = sum(card_counts)
    print("Part 2:" + str(ans))


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()
    solve_part1()
    solve_part2()
