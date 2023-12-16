from utils import *
from collections import defaultdict
from tqdm import tqdm

grid = read_lines()
# grid = r""".|...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\
# ..../.\\..
# .-.-/..|..
# .|....-|.\
# ..//.|....""".splitlines()

def step(grid, i, j, di, dj, visited):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return []
    if (di, dj) in visited[i, j]:
        return []
    visited[i, j].add((di, dj))
    match grid[i][j]:
        case '/':
            di, dj = -dj, -di
        case '\\':
            di, dj = dj, di
        case '|' if dj:
            return [(i, j, -1, 0), (i, j, 1, 0)]
        case '-' if di:
            return [(i, j, 0, -1), (i, j, 0, 1)]
    return [(i + di, j + dj, di, dj)]

def trace(grid, beams):
    visited = defaultdict(set)
    while beams:
        for beam in step(grid, *beams.pop(), visited):
            beams.append(beam)
            # print(beam)
            # print('\n'.join(''.join('^v<>'[(beam[2]+1)//2 if beam[2] else (beam[3]+5)//2]
            #                         if (i, j) == beam[:2] else c if (i, j) not in visited 
            #                         else '#' for j, c in enumerate(row)) 
            #                 for i, row in enumerate(grid)), end='\n\n')
    return visited

print(len(trace(grid, [(0, 0, 0, 1)])))

starts = []
for i in range(len(grid)):
    starts.append((i, 0, 0, 1))
    starts.append((i, len(grid[0])-1, 0, -1))
for j in range(len(grid[0])):
    starts.append((0, j, 1, 0))
    starts.append((len(grid)-1, j, -1, 0))

print(max(len(trace(grid, [start])) for start in tqdm(starts)))
