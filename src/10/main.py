import math

def find_start():
    for i, line in enumerate(lines):
        j = line.find("S")
        if j >= 0:
            return i,j

def at(x,y):
    return grid[x][y]

def towards(direction, pos):
    x,y = pos
    #print(f"Input to towards: {direction}, {pos}")
    match direction: 
        case 'N': 
            new_x, new_y = x-1, y
            return (at(new_x, new_y), (new_x, new_y)) if new_x >= 0 else ('x',  (new_x, new_y))
        case 'S':
            new_x, new_y = x+1, y
            return (at(new_x, new_y), (new_x, new_y)) if new_x < len(grid) else ('x',  (new_x, new_y))
        case 'E': 
            new_x, new_y = x, y+1
            return (at(new_x, new_y), (new_x, new_y)) if new_y < len(grid[0]) else ('x',  (new_x, new_y))
        case 'W':
            new_x, new_y = x, y -1
            return (at(new_x, new_y), (new_x, new_y)) if new_y >= 0 else ('x',  (new_x, new_y))

conn_map = {
    "|" : ['N', 'S'],
    "7" : ['W', 'S'],
    'F' : ['S', 'E'],
    '-' : ['E', 'W'],
    'L' : ['N', 'E'],
    'J' : ['W', "N"],
    'N' : '7|FS',
    'S' : '|LJS',
    'E' : '-7JS', 
    'W' : '-LFS'
 }

def get_next_pos(pos, prev_pos, from_start=False):
    x,y = pos
    current_tile = at(x,y)
    possible_directions = conn_map[current_tile] if not from_start else ['N','S','E','W']
    for dir in possible_directions:
        next_tile, new_pos = towards(dir, pos)
        if next_tile in conn_map[dir] and prev_pos != new_pos:
            return new_pos,next_tile


def find_loop_length(start):
    x,y = start
    tile_type = at(x,y)
    loop = {start:tile_type}
    current_pos, current_tile = get_next_pos(start,None,from_start=True)
    loop[current_pos] = current_tile
    prev_pos = start
    steps = 1 
    while current_pos != start: 
        temp = current_pos
        current_pos, current_tile= get_next_pos(current_pos, prev_pos)
        loop[current_pos] = current_tile
        prev_pos = temp
        steps += 1
        #print(f"New Pos: {current_pos}, Steps: {steps}")
    return steps, loop

# crossing_counter = {
#     'N' : ['JF', 'L7'],
#     'S' : ['FJ', '']

# }

def count_of_loop_crossings(dir, point):
    x,y = point
    crossings = 0
    tile = at(x,y)
    n_s_pending = None
    e_w_pending = None
    while tile != 'x':
        #print(tile, point, dir)
        tile, point = towards(dir, point)
        if point not in loop:
            continue
        if dir == 'N' and tile != "|":
            if not n_s_pending and tile == "-":
                crossings += 1
            elif (n_s_pending == 'J' and tile == 'F') or (n_s_pending == "L" and tile == '7'):
                crossings += 1
                n_s_pending = None
            elif (n_s_pending == 'L' and tile == 'F') or (n_s_pending == 'J' and tile == '7'): 
                n_s_pending = None
            else:
                n_s_pending = tile
        if dir == 'S' and tile != "|":
            if not n_s_pending and tile == "-":
                crossings += 1
            elif (n_s_pending == 'F' and tile == 'J') or (n_s_pending == '7' and tile == 'L'): 
                crossings += 1
                n_s_pending = None
            elif (n_s_pending == 'F' and tile == 'L') or (n_s_pending == '7' and tile == 'J') :
                n_s_pending = None
            else: 
                n_s_pending = tile
        if dir == 'E' and tile != '-': 
            if x == 69 and y == 63:
                print(f"Before: x: {x}, y:{y}, point: {point}, e-w-pending: {e_w_pending}, tile: {tile}, crossings: {crossings} ")
            if not e_w_pending and tile == "|":
                crossings += 1
            elif (e_w_pending == 'L' and tile == '7') or (e_w_pending == 'F' and tile == 'J'): 
                crossings+= 1
                e_w_pending = None
            elif (e_w_pending == 'L' and tile == 'J') or (e_w_pending == 'F' and tile == '7'):
                e_w_pending = None
            else:
                e_w_pending = tile 
            if x == 69 and y == 63:
                print(f"After: x: {x}, y:{y}, point: {point}, e-w-pending: {e_w_pending}, tile: {tile}, crossings: {crossings} ")

        if dir  == 'W' and tile != '-': 
            if not e_w_pending and tile == "|":
                crossings += 1
            elif (e_w_pending == 'J' and tile == 'F') or (e_w_pending == '7' and tile == 'L'):
                crossings += 1
                e_w_pending = None
            elif (e_w_pending == 'J' and tile == 'L') or (e_w_pending == '7' and tile == 'F'):
                e_w_pending = None
            else: 
                e_w_pending = tile 

    print(f"Point: {x},{y}, Dir: {dir}, Crossings: {crossings}")
    return crossings


def calculate_tiles_inside_loop():
    """Logic: In order to be in the loop there should be an odd no. of loop crossings in each direction."""
    count_inside = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])): 
            if (i,j) in loop:
                continue
            is_inside = True
            for dir in ['N','S','E', 'W']:
                if count_of_loop_crossings(dir, (i,j)) % 2 == 0: 
                    is_inside = False
                    break
            if is_inside:
                count_inside += 1
                points_in_loop[(i,j)] = at(i,j)
    return count_inside

def print_loop():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i,j) in loop:
                match grid[i][j]:
                    case "7":
                        print("\u2510",end="")
                    case "J":
                        print("\u2518",end="")
                    case "L":
                        print("\u2514",end="")
                    case "F": 
                        print("\u250C",end="")
                    case "|":
                        print("\u2502",end="")
                    case "-":
                        print("\u2500",end="")
                    case _: 
                        print(grid[i][j],end="")
            elif (i,j) in points_in_loop:
                    print("I", end='')
            else:
                print(grid[i][j],end="")
        print("\n",end="")

with open("input.txt", "r", encoding="UTF8") as f: 
    lines = f.read().splitlines()

grid = [[c for c in line] for line in lines]

start_pos = find_start()

loop_length, loop = find_loop_length(start_pos)
points_in_loop = {}

part2 = calculate_tiles_inside_loop()


for point in points_in_loop:
    for dir in ['N', 'S', 'E', 'W']: 
        crossings = count_of_loop_crossings(dir, point)
        print(f"Point: {point}, Dir: {dir}, Crossings: {crossings}")


print(f"Part 2: {part2}")
print(f"Part 1: {math.ceil(loop_length/2)}")

print_loop()

