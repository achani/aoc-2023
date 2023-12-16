""""""
from collections import deque


def move_beam(beam): 
    d = beam[1]
    r,c = beam[0][0], beam[0][1]
    d_new = d
    
    tile = grid[r][c]
    if d in ['r','l'] and tile == '|':
        #split the beam
        beams.extend([((r,c),'u'), ((r,c), 'd')])
        return None 
    if d in ['u','d'] and tile == "-":
        beams.extend([((r,c),'l'), ((r,c), 'r')])
        return None 
    if tile in ['/','\\']: 
        d_new = turns[tile][d] 
    offset = offsets[d_new]
    next_r, next_c = r+offset[0] , c+offset[1]
    if not (0<= next_r<R and 0<= next_c < C):
        #The beam is leaving he grid, let's not follow it any more. 
        return None
    else:
        return ((next_r,next_c), d_new)

def record_tile_activation(beam):
    d = beam[1]
    r,c = beam[0][0], beam[0][1]
    new_activation = True
    if (r,c) not in tile_activation:
        tile_activation[(r,c)] = [d]
    elif d not in tile_activation[(r,c)]:
        tile_activation[(r,c)].append(d)
    else:
        new_activation = False
    return not new_activation 

with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()

grid = [[c for c in row] for row in lines]
R, C = len(grid), len(grid[0])
tile_activation = {}

offsets = {'r': (0,1), 'l': (0,-1), 'u': (-1,0), 'd': (1, 0)}

turns = {'\\': { 'r': 'd','l': 'u', 'u': 'l', 'd': 'r'},
         '/': {'r': 'u', 'l': 'd', 'u': 'r', 'd': 'l'}
        }

beams = deque([((0,0),"r")])
while len(beams) > 0: 
    beam = beams.popleft()
    while beam:
        already_traced = record_tile_activation(beam)
        if not already_traced:
            beam = move_beam(beam)
        else: 
            beam = None
        

print(len(tile_activation.keys()))
