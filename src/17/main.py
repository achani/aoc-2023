
"""
Ref: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
procedure uniform_cost_search(start) is
    node ← start
    frontier ← priority queue containing node only
    expanded ← empty set
    do
        if frontier is empty then
            return failure
        node ← frontier.pop()
        if node is a goal state then
            return solution(node)
        expanded.add(node)
        for each of node's neighbors n do
            if n is not in expanded and not in frontier then
                frontier.add(n)
            else if n is in frontier with higher cost
                replace existing node with n
"""
from queue import PriorityQueue

#Direction of movement can be Forward, Left or Right as Backward is not allowed. 
#We need to ensure there are only max "N" steps in a direction beyond which we must turn. 
#We need to take care of these conditions when deciding which are the next possible neighbors. 
#Part 2 adds requirements for min steps forward before it is allowed to turn
def get_neighbors(node, min_forward_steps, max_forward_steps):
  neighbors = []
  loss, r,c,r_prv, c_prv, forward_steps = node
  #start position, can go only right or down. 
  if r == c == 0: 
    neighbors.append((loss + grid[r][c + 1], r, c+1, r,c, 1))
    neighbors.append((loss + grid[r + 1][c], r+1, c, r,c, 1))
    return neighbors
  #Add forward if allowed
  if forward_steps < max_forward_steps:
      r_nxt = r + (r - r_prv)
      c_nxt = c + (c - c_prv)
      if 0 <= r_nxt < R and 0 <= c_nxt < C: 
        neighbors.append((loss + grid[r_nxt][c_nxt], r_nxt, c_nxt, r, c, forward_steps+1))
  #Cannot turn till min forward step requirement is met.
  if forward_steps < min_forward_steps:
    return neighbors
  #Add left and right
  offsets=[]
  if c == c_prv:
    offsets.extend([(0,1), (0,-1)])
  if r == r_prv:
    offsets.extend([(1,0), (-1,0)])
  for r_offset, c_offset in offsets:
    r_nxt = r + r_offset
    c_nxt = c + c_offset
    if 0 <= r_nxt < R and 0 <= c_nxt < C: 
      neighbors.append((loss + grid[r_nxt][c_nxt], r_nxt, c_nxt, r,c, 1))
  return neighbors


def uniform_cost_search(src, dest, min_forward_steps, max_forward_steps, min_steps_to_stop):
  src_r,src_c = src
  dest_r, dest_c = dest
  frontier = PriorityQueue()
  frontier.put((0, src_r,src_c, None, None, 0))
  expanded = set()
  while True:
    if frontier.empty():
      raise Exception("No Solution possible.")
    current = frontier.get()
    hl, r, c, _, _, steps_forward = current
    if r == dest_r and c == dest_c and steps_forward >= min_steps_to_stop:
      return hl
    if current[1:] in expanded:
      continue
    else:
      expanded.add(current[1:])
    neighbors = get_neighbors(current, min_forward_steps, max_forward_steps)
    for new_node in neighbors: 
      frontier.put(new_node)


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()

grid = [[int(c) for c in row] for row in lines]
R, C = len(grid), len(grid[0])
start,dest = (0,0), (R-1,C-1)
print(f"Part 1: {uniform_cost_search(start, dest, 1, 3, 1)}")
print(f"Part 2: {uniform_cost_search(start, dest, 4, 10, 4)}")
