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

def run(grid, steps):
    poses = set((i, j) for i, row in enumerate(grid) 
                for j, char in enumerate(row) if char == 'S')
    n_grids = 1
    res = []
    for t in range(steps):
        poses = step(grid, poses)
        g = len(set(p[2:] for p in poses))
        res.append([t+1, len(poses), g])
        if g > n_grids:
            print("step", t+1, "cells", len(poses), "grids", n_grids)
            n_grids = g
    return res

print(run(grid, 64)[-1][1])

# %%
def neighbors(grid, i, j, m=0, n=0):
    i, j = i + m * M, j + n * N
    return ((ii, jj, mm, nn) for di, dj in dirs
            for mm, ii in [divmod(i + di, M)]
            for nn, jj in [divmod(j + dj, N)]
            if grid[ii][jj] != '#')

data = run(grid, M*5//2+1)

# %%
import numpy as np

data = np.array([data[i] for i in range(len(data)-1) if data[i][2] < data[i+1][2]])
print(data)
# the rate of growth is linear, so we can fit a quadratic polynomial
# t = (65 + 66) * i + 65, i = 0, 1, 2
coefs = np.polyfit(data[::2, 0], data[::2, 1], 2)
print(coefs, np.polyval(coefs, 26501365))
# 26501365 = 2023 * (65 + 66) * 100 + 65
