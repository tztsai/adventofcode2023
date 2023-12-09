from utils import *

lines = read_lines()
bag = dict(red = 12, green = 13, blue = 14)

def parse(game):
    i, game = re.match(r'Game (\d+): (.*)', game).groups()
    sets = game.split('; ')
    pat = re.compile(r'(\d+) (\w+)')
    return int(i), [{color: int(num) for num, color in pat.findall(s)} for s in sets]

def check(game):
    i, sets = parse(game)
    for cubes in sets:
        if any(cubes[color] > bag[color] for color in cubes):
            return 0
    return i

print(sum(check(game) for game in lines))

def power(game):
    _, sets = parse(game)
    p = 1
    for color in bag:
        p *= max(s.get(color, 0) for s in sets)
    return p

print(sum(power(game) for game in lines))