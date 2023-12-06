from functools import lru_cache



def evaluate_card_part1(card):
    card_values = card.split(":")[1]
    parts = card_values.split("|")
    winning_nos, my_nos = parts[0].split(), parts[1].split()
    matching_nos = list(set(winning_nos) & set(my_nos))

    print(card) 
    
    ans = (2 ** (len(matching_nos) - 1)) if len(matching_nos) > 0 else 0 
    print(f'{",".join(matching_nos)} ({len(matching_nos)}) ==> {ans}')
    return ans

@lru_cache(maxsize=None)
def evaluate_card_part2(card_no):
    card = lines[card_no]
    card_values = card.split(":")[1]
    parts = card_values.split("|")
    winning_nos, my_nos = parts[0].split(), parts[1].split()
    matching_nos = list(set(winning_nos) & set(my_nos))
    print(matching_nos)
    return len(matching_nos)


def solve_part1():
    ans = 0
    for line in lines: 
       ans += evaluate_card_part1(line)
    print("Part 1: " + str(ans))



queue = []


def solve_part2():
    ans = 0
    queue = [i for i in range(len(lines))]
    counter = 0
    while len(queue) > 0: 
        
        card = queue.pop(0)
        matches = evaluate_card_part2(card)
        for i in range(matches): 
            queue.append(i+card+1)
        ans += 1
        if ans % 50000 == 0:
            print(f"Processed card {card}. Matches: {(matches)} Add card no. {i+card+1}. | Queue Length: {len(queue)} | Current Total : {ans}")
        
    print("Part 2:" + str(ans))

lines = None
with open("input.txt", 'r') as f:
    lines = f.read().splitlines()
    solve_part1()
    solve_part2()
