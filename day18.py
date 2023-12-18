from utils import *
from collections import defaultdict

lines = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines()
lines = read_lines()

pattern = re.compile(r"([UDLR]) (\d+) \((.*)\)")

directions = dict(U=(-1, 0), D=(1, 0), L=(0, -1), R=(0, 1))

def dig(path, pos, dir, steps):
    pos = pos[0] + dir[0] * steps, pos[1] + dir[1] * steps
    path.append(pos)
    return pos

def parse_line(line):
    dir, steps, color = pattern.match(line).groups()
    return dir, int(steps), color

def measure(plan):
    path = []
    border = 0
    pos = (0, 0)
    for line in plan:
        dir, steps, color = parse_line(line)
        pos = dig(path, pos, directions[dir], steps)
        border += steps
    path.append(path[0])
    A = sum(i1*j2 - i2*j1 for (i1, j1), (i2, j2) in zip(path, path[1:])) / 2
    return int(abs(A) + border / 2 + 1)  # Pick's theorem (including border) (see also day10.py)

print(measure(lines))

def parse_line(line):
    _, _, code = pattern.match(line).groups()
    dir = 'RDLU'[int(code[-1])]
    steps = int('0x' + code[1:-1], 16)
    return dir, steps, None

print(measure(lines))