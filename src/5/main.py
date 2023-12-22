import math

def parse_map(map):
  lines = map.splitlines()[1:] #ignore the first line with the name of the map. 
  return [tuple([int(i) for i in line.split()]) for line in lines]


def map_single_seed(seed, map): 
  for (dest, start, size) in map: 
    if seed >= start and seed <= start+size: 
      return dest + seed - start
  return seed


def map_seed_ranges(ranges, map):
  maped_ranges = []
  pending_ranges = ranges
  for (dest, mp_start, size) in map:
    not_matched= []
    mp_end = mp_start+size
    for (rng_start, rng_end) in pending_ranges: 
      if rng_start >= mp_start and rng_end <= mp_end:
        #input range is completely within the map range
        maped_ranges.append((dest+rng_start-mp_start, dest+rng_end-mp_start))
      elif rng_start < mp_start and rng_end <= mp_start:
        #complete input range is to the left of map range (no overlap)
        not_matched.append((rng_start,rng_end))
      elif rng_start >= mp_end and rng_end > mp_end:
        #complete input range is to the right of the map range (no overlap)
        not_matched.append((rng_start,rng_end))
      elif rng_start < mp_start and rng_end >= mp_start:
        # overlap on the left side
        not_matched.append((rng_start, mp_start))
        maped_ranges.append((dest, dest+rng_end - mp_start))
      elif rng_start >= mp_start and rng_end > mp_end:
        # overlap on the right side
        maped_ranges.append((dest+rng_start-mp_start, dest+mp_end-mp_start))
        not_matched.append((mp_end, rng_end))
      elif rng_start < mp_start and rng_end > mp_end:
        #overlap on both sides 
        not_matched.append((rng_start, mp_start))
        not_matched.append((mp_end, rng_end))
        maped_ranges.append((dest, dest+mp_end-mp_start))
    pending_ranges = not_matched
  return maped_ranges + pending_ranges

def solve_part1():
  ans = math.inf
  for seed in seeds: 
    for map in maps: 
      seed = map_single_seed(seed, map)
    ans = seed if seed < ans else ans
  return ans


def solve_part2():
  seed_pairs = [(seeds[i],seeds[i+1]) for i in range(0,len(seeds),2)]
  min_value = math.inf
  outputs = []
  for start, sz in seed_pairs:
    current_ranges = [(start, start + sz)]
    for map in maps: 
      current_ranges = map_seed_ranges(current_ranges, map)
    outputs.extend(current_ranges)
  min_location = math.inf
  for output_rng_start, _ in outputs: 
    if output_rng_start < min_location:
      min_location = output_rng_start
  return min_location

with open("input.txt", "r") as f: 
  seeds, *maps_raw = f.read().split("\n\n")

seeds = [int(s) for s in seeds.split(":")[1].split()]
maps = [parse_map(map) for map in maps_raw]

print(f"Part 1: {solve_part1()}")
print(f"Part 2: {solve_part2()}")
