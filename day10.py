from utils import *

def find_start(grid):
    return next((i, j) for i, row in enumerate(grid) 
                for j, char in enumerate(row) if char == 'S')

pipes = {
    '|': {(1, 0), (-1, 0)},
    '-': {(0, 1), (0, -1)},
    'L': {(-1, 0), (0, 1)},
    'J': {(-1, 0), (0, -1)},
    '7': {(1, 0), (0, -1)},
    'F': {(1, 0), (0, 1)},
}

dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

def neighbors(grid, i, j):
    c = grid[i][j]
    for di, dj in (dirs if c == 'S' else pipes[c]):
        if 0 <= i + di < len(grid) and 0 <= j + dj < len(grid[0]):
            yield (i + di, j + dj)

def find_next(grid, path, dists):
    i, j = path[-1]
    for ni, nj in neighbors(grid, i, j):
        if (ni, nj) not in dists:
            if (i - ni, j - nj) in pipes.get(grid[ni][nj], []):
                return (ni, nj)

grid = read_lines()
start = find_start(grid)
path = [start]
dists = {start: 0}
while (pos := find_next(grid, path, dists)):
    dists[pos] = dists[path[-1]] + 1
    path.append(pos)

print((max(dists.values()) + 1) // 2)

def calc_enclosed_area(path):
    path = path + [path[0]]
    # https://brilliant.org/wiki/area-of-a-polygon/
    A = sum(i1*j2 - i2*j1 for (i1, j1), (i2, j2) in zip(path, path[1:])) / 2
    b = len(path) - 1
    # https://artofproblemsolving.com/wiki/index.php/Pick%27s_Theorem
    return abs(A) - b / 2 + 1

print(calc_enclosed_area(path))