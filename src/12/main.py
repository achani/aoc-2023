from functools import lru_cache
from collections import deque


def count_possibilities(condition_record,num_groups):
  key = tuple((condition_record, tuple(num_groups)))
  if key in CACHE:
    return CACHE[key]
  
  if condition_record == "":
    if len(num_groups)  == 0: 
      return 1
    else:
      return 0
  
  if len(num_groups) == 0:
    if "#" in condition_record:
      return 0
    else:
      return 1
  
  if (condition_record.count('?') + condition_record.count('#') < sum(num_groups)):
    return 0

  ans = 0
  if condition_record[0] == "?":
    # '?' can be either a '.' or a '#'
    ans += count_possibilities(condition_record[1:], num_groups)
    if "." not in condition_record[:num_groups[0]] and (len(condition_record) == num_groups[0] or condition_record[num_groups[0]] in ".?" ): 
      ans += count_possibilities(condition_record[num_groups[0] + 1:], num_groups[1:] )
  if condition_record[0] == ".":
    ans += count_possibilities(condition_record[1:], num_groups)
  if condition_record[0] == "#" and "." not in condition_record[:num_groups[0]] and (len(condition_record) == num_groups[0] or condition_record[num_groups[0]] in ".?" ): 
    ans += count_possibilities(condition_record[num_groups[0] + 1:], num_groups[1:] )

  CACHE[key] = ans
  return ans


CACHE = {}

def process_line_part1(input):
  condition_record, num_groups = input.split()
  num_groups = num_groups.split(",")
  num_groups = [int(x) for x in num_groups]

  return count_possibilities(condition_record, num_groups)


def process_line_part2(input):
  condition_record, num_groups = input.split()
  num_groups = num_groups.split(",")
  num_groups = [int(x) for x in num_groups]
  condition_record = "?".join([condition_record]*5)
  num_groups = num_groups * 5
  return count_possibilities(condition_record, num_groups)


with open("input.txt", "r", encoding="UTF8") as f:
  lines = f.read().splitlines()

part1 = sum([process_line_part1(line) for line in lines])
part2 = sum([process_line_part2(line) for line in lines])
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")



