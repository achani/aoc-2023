from copy import deepcopy


def execute_workflow(rating, conditions):
  for condition in conditions[:-1]: 
    result = condition.split(":")[1]
    param, oper, val = condition[0],condition[1],condition.split(":")[0][2:]
    val = int(val)
    match oper: 
      case "<":
        if rating[param] < val:
          return result
      case ">":
        if rating[param] > val: 
          return result
  return conditions[-1]


def intersect_ranges(r1,r2):
  r1_low, r1_high = r1
  r2_low, r2_high = r2
  low = max(r1_low, r2_low)
  high = min(r1_high, r2_high)
  return (low,high) if high > low else None


def get_acceptable_ranges(current_range,workflow):
  conditions = workflows[workflow]
  acc_ranges=[]
  #Example: px{a<2006:qkq,m>2090:A,rfg}
  for condition in conditions[:-1]:
    result = condition.split(":")[1]
    param, oper, val = condition[0],condition[1],condition.split(":")[0][2:]
    val = int(val)
    match oper: 
      case "<":
        param_range_true = intersect_ranges(current_range[param], (1,val))
        param_range_false = intersect_ranges(current_range[param], (val,4001))
      case ">":
        param_range_true = intersect_ranges(current_range[param], (val+1,4001))
        param_range_false = intersect_ranges(current_range[param], (1, val+1))

    if param_range_true and result != "R":
      current_range[param] = param_range_true
      if result == "A": 
        acc_ranges.append(deepcopy(current_range))
      else:
        acc_ranges.extend(get_acceptable_ranges(deepcopy(current_range), result))
    if param_range_false: 
      current_range[param] = param_range_false
    else:
      return acc_ranges
  #handle final catch-all decision
  if param_range_false and conditions[-1] != "R":
    if conditions[-1] == "A":
      acc_ranges.append(deepcopy(current_range))
    else:
      acc_ranges.extend(get_acceptable_ranges(deepcopy(current_range),conditions[-1]))
  return acc_ranges


def solve_part1():
  accepted_components = []
  for i, rating in enumerate(ratings): 
    result = "in"
    while result not in ["A", "R"]:
      workflow = workflows[result]
      result = execute_workflow(rating, workflow)
    if result == "A":
      accepted_components.append(i)
  ans = 0
  for i in accepted_components:
    ans += sum(ratings[i].values())

  print(f"Part 1: {ans}")


def solve_part2():
  workflow = "in"
  current_range = {"x": (1, 4001), "m": (1, 4001) , "a": (1, 4001), "s": (1, 4001)}

  ans = 0 
  acceptable_ranges = get_acceptable_ranges(current_range, workflow)
  for rng in acceptable_ranges:
    ans += (rng["x"][1] - rng["x"][0]) * (rng["m"][1] - rng["m"][0]) * (rng["a"][1] - rng["a"][0]) * (rng["s"][1] - rng["s"][0])
  print(f"Part 2: {ans}")


with open("input.txt", "r") as f:
  workflow_data, ratings_data = f.read().split("\n\n")

workflows = {}
ratings = []
for workflow in workflow_data.split("\n"):
  id, conditions = workflow.split("{")
  conditions = conditions[:-1].split(",")
  workflows[id] = conditions

for rating in ratings_data.split("\n"):
  rating_parts= rating[1:-1].split(",")
  rating_parsed = {}
  for part in rating_parts:
    k,v = part.split("=")
    rating_parsed[k] = int(v)
  ratings.append(rating_parsed)


solve_part1()
solve_part2()
