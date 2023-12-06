
#Config of bag Red, Green, Blue cubes count [R,G,B]
bag_config = [12,13,14]
#Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
def validate_game_part1(game): 
    parts = game.split(':')
    game_id = parts[0].split(" ")[1]
    draws = parts[1].split(";")
    draws = list(map(lambda x: x.split(','), draws))
    
    for draw in draws: 
        r= g= b = 0
        for color in draw: 
            color = color.strip().split(" ")
            
            if(color[1] == 'red'):
             r = int(color[0])
            elif(color[1] == 'green'):
             g = int(color[0])
            elif(color[1] == "blue"):
             b = int(color[0])
        if r > bag_config[0] or g > bag_config[1] or b > bag_config[2]:
            return 0

    return int(game_id)

#Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
def validate_game_part2(game): 
    parts = game.split(':')
    game_id = parts[0].split(" ")[1]
    draws = parts[1].split(";")
    draws = list(map(lambda x: x.split(','), draws))
    
    r_min = g_min = b_min = 1

    for draw in draws: 
        r= g= b = 0
        for color in draw: 
            color = color.strip().split(" ")
            if(color[1] == 'red'):
             r = int(color[0])
            elif(color[1] == 'green'):
             g = int(color[0])
            elif(color[1] == "blue"):
             b = int(color[0])
        if r > r_min: 
           r_min = r
        if g > g_min:
           g_min =g 
        if b > b_min: 
           b_min = b

    return r_min * g_min * b_min


def solve_part1():
    ans = 0
    for line in lines: 
       value = validate_game_part1(line)
       ans += value
       #print(line, value )
    print("Part 1: " + str(ans))



def solve_part2():
    ans = 0
    for line in lines: 
       value = validate_game_part2(line)
       ans += value
    print("Part 2" + str(ans))

lines = None
with open("input.txt", 'r') as f:
    lines = f.read().splitlines()
    solve_part1()
    solve_part2()
