

def get_hash(input):
  hash = 0
  for c in input: 
    hash = ((hash + ord(c)) * 17) % 256
  return hash


def perform_step(hash,label,opeartion, focal_length):
  box = boxes[hash]
  if operation == "REMOVE":
    for i,lens in enumerate(box): 
      if lens[0] == label: 
        box.pop(i)
  if operation == "ADD":
    found = False
    for i, lens in enumerate(box):
      if lens[0] == label: 
        found = True
        box[i] = tuple((label, focal_length))
    if not found:
      box.append(tuple((label, focal_length)))


with open("input.txt", "r") as f: 
  steps = f.read().split(",")

boxes = [ [] for _ in range(256)]

part1 = sum([get_hash(step) for step in steps])
print(f"Part 1: {part1}")
 
for step in steps: 
  focal_length = None
  if "-" in step: 
    label = step.split("-")[0]
    operation = "REMOVE"
  if "=" in step:
    label,focal_length = step.split("=")
    focal_length = int(focal_length)
    operation = "ADD"
  hash = get_hash(label)
  perform_step(hash,label,operation,focal_length)

part2 = 0 
for box_num, box in enumerate(boxes): 
  for len_num, (_,focal_length) in enumerate(box):
    part2 += (box_num+1) * (len_num+1) * focal_length

print(f"Part 2: {part2}")