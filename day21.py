# %%
from utils import *

grid = read_input('day21.txt')

M = len(grid)
N = len(grid[0])

dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

def neighbors(grid, i, j):
    return ((i + di, j + dj) for di, dj in dirs
            if 0 <= i + di < len(grid) and 0 <= j + dj < len(grid[0])
            if grid[i + di][j + dj] != '#')

def step(grid, poses):
    return set(nb for p in poses for nb in neighbors(grid, *p))

def run(grid, steps, expansion_points=[]):
    poses = set((i, j) for i, row in enumerate(grid) 
                for j, char in enumerate(row) if char == 'S')
    traces = []
    for t in range(steps):
        poses = step(grid, poses)
        cells = {p[2:]: [] for p in poses}
        for p in poses:
            cells[p[2:]].append(p[:2])
        if traces and len(cells) > len(traces[-1]):
            print(t+1, len(poses))
            expansion_points.append(t+1)
        traces.append(sorted((k, len(v)) for k, v in cells.items()))
    print(t+1, len(poses))
    return traces

run(grid, 64)

# %%
def neighbors(grid, i, j, m=0, n=0):
    i, j = i + m * M, j + n * N
    return ((ii, jj, mm, nn) for di, dj in dirs
            for mm, ii in [divmod(i + di, M)]
            for nn, jj in [divmod(j + dj, N)]
            if grid[ii][jj] != '#')

expansion_points = []
traces = run(grid, M*5//2+1, expansion_points)

import json
with open('day21.json', 'w') as f:
    json.dump(traces, f)

# %%
import numpy as np

data = np.array([[i-1, sum(n for _, n in traces[i-2])] for i in expansion_points[::2]])
print(data)
# the rate of growth is linear, so we can fit a quadratic polynomial
# t = (65 + 66) * i + 65, i = 0, 1, 2
coefs = np.polyfit(data[:, 0], data[:, 1], 2)
print(np.polyval(coefs, 26501365))
# 26501365 = 2023 * (65 + 66) * 100 + 65
