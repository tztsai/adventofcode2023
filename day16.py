from utils import *
from collections import defaultdict
from tqdm import tqdm

grid = read_input()
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

def trace(grid, i, j, di, dj):
    beams = [(i, j, di, dj)]
    visited = defaultdict(set)
    while beams:
        i, j, di, dj = beams.pop()
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or (di, dj) in visited[i, j]:
            continue
        visited[i, j].add((di, dj))
        match grid[i][j]:
            case '/':
                di, dj = -dj, -di
            case '\\':
                di, dj = dj, di
            case '|' if dj:
                beams.extend([(i-1, j, -1, 0), (i+1, j, 1, 0)])
                continue
            case '-' if di:
                beams.extend([(i, j-1, 0, -1), (i, j+1, 0, 1)])
                continue
        beams.append((i + di, j + dj, di, dj))
    return visited

print(len(trace(grid, 0, 0, 0, 1)))

starts = []
for i in range(len(grid)):
    starts.append((i, 0, 0, 1))
    starts.append((i, len(grid[0])-1, 0, -1))
for j in range(len(grid[0])):
    starts.append((0, j, 1, 0))
    starts.append((len(grid)-1, j, -1, 0))

print(max(len(trace(grid, *start)) for start in tqdm(starts)))
