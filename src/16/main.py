""""""
from collections import deque


def get_activation(beam):
    # beams = deque([((0,0),"r")])
    beams = deque([beam])
    tile_activation = {}

    def move_beam(beam):
        d = beam[1]
        r, c = beam[0][0], beam[0][1]
        d_new = d

        tile = grid[r][c]
        if d in ["r", "l"] and tile == "|":
            # split the beam
            beams.extend([((r, c), "u"), ((r, c), "d")])
            return None
        if d in ["u", "d"] and tile == "-":
            beams.extend([((r, c), "l"), ((r, c), "r")])
            return None
        if tile in ["/", "\\"]:
            d_new = turns[tile][d]
        offset = offsets[d_new]
        next_r, next_c = r + offset[0], c + offset[1]
        if not (0 <= next_r < R and 0 <= next_c < C):
            # The beam is leaving he grid, let's not follow it any more.
            return None
        else:
            return ((next_r, next_c), d_new)

    def record_tile_activation(beam):
        d = beam[1]
        r, c = beam[0][0], beam[0][1]
        new_activation = True
        if (r, c) not in tile_activation:
            tile_activation[(r, c)] = [d]
        elif d not in tile_activation[(r, c)]:
            tile_activation[(r, c)].append(d)
        else:
            new_activation = False
        return not new_activation

    while len(beams) > 0:
        beam = beams.popleft()
        while beam:
            already_traced = record_tile_activation(beam)
            if not already_traced:
                beam = move_beam(beam)
            else:
                beam = None
    return len(tile_activation.keys())


def get_max_activation(beams):
    max_activation = 0
    for beam in beams:
        act = get_activation(beam)
        # print(f"{act=}, {max_activation=}")
        max_activation = max(act, max_activation)
    return max_activation


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()

grid = [[c for c in row] for row in lines]
R, C = len(grid), len(grid[0])


offsets = {"r": (0, 1), "l": (0, -1), "u": (-1, 0), "d": (1, 0)}

turns = {
    "\\": {"r": "d", "l": "u", "u": "l", "d": "r"},
    "/": {"r": "u", "l": "d", "u": "r", "d": "l"},
}


initial_beam_positions = []
for i in range(C):
    if i == 0:
        initial_beam_positions.extend([((0, 0), "r"), ((R - 1, 0), "r")])
    if i == C - 1:
        initial_beam_positions.extend([((0, i), "l"), ((R - 1, i), "l")])
    initial_beam_positions.extend([((0, i), "d"), ((R - 1, i), "u")])


print(f"Part 1: {get_activation(((0,0),'r'))}")
print(f"Part 2: {get_max_activation(initial_beam_positions)}")
