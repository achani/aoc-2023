from pathlib import Path

input_path = Path(__file__).parent.parent / "input" / "day01.txt"
digits = {'1':1, '2': 2, '3': 3, '4':4, '5':5, '6': 6, '7':7, '8':8, '9':9, '0':0, 
              'one':1, 'two':2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight':8,'nine':9, 'zero': 0 }
digits_r = {k[::-1]:v  for k,v in digits.items()}
def find_match(input, d):
    i = 0
    while i < len(input):
        for k in d.keys(): 
            if input[i:].startswith(k):
                return d[k]
        i += 1


with open(input_path, 'r') as f:
    lines = f.read().splitlines()
    ans = 0
    for line in lines: 
        #print(line + ": ", end="")
        value = find_match(line, digits) * 10 + find_match(line[::-1], digits_r)
        #print(value)
        ans += value
print(ans)
