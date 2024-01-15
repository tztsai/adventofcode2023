# %%
from utils import *
from collections import defaultdict
from itertools import product

lines = read_input()

def parse_brick(line):
    return list(map(sorted, zip(
        *[map(int, p.split(',')) for p in line.split('~')])))

def find_bricks_below(bricks):
    bricks.sort(key=lambda b: b[2][0])
    occupies = defaultdict(list)
    belows = defaultdict(set)
    for i, brick in enumerate(bricks):
        (x_lo, x_hi), (y_lo, y_hi) = brick[:2]
        for x, y in product(range(x_lo, x_hi+1), range(y_lo, y_hi+1)):
            bricks_below = occupies[x, y]
            belows[i].update(bricks_below)
            bricks_below.append(i)
    return belows

def fall_down(bricks, belows):
    for i, js in belows.items():  # belows should be topologically sorted
        z_lo, z_hi = bricks[i][2]
        max_z_below = max(bricks[j][2][1] for j in js) if js else 0
        bricks[i][2] = [max_z_below + 1, max_z_below + z_hi - z_lo + 1]

def make_graph(bricks, belows):
    graph = {i: set() for i in [-1, *belows]}
    for i, js in reversed(belows.items()):
        for j in js or [-1]:  # node -1 for the ground (no brick below i)
            if j < 0 or bricks[i][2][0] == bricks[j][2][1] + 1:
                graph[j].add(i)  # j is supporting i
    return graph  # graph[j] = bricks supported by j

def count_falling(graph):
    n_falling = {}
    for i in reversed(graph):  # from top to bottom
        if i < 0:
            return n_falling
        visited = {i}
        stack = [-1]
        # BFS to find reachable bricks from the ground
        while stack:
            b = stack.pop()
            visited.add(b)
            stack.extend(graph[b] - visited)
        n_falling[i] = len(graph) - len(visited)

bricks = list(map(parse_brick, lines))
belows = find_bricks_below(bricks)
fall_down(bricks, belows)
graph = make_graph(bricks, belows)
fallings = count_falling(graph)

print(sum(n == 0 for n in fallings.values()))
print(sum(n for n in fallings.values()))
