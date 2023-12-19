from utils import *
import heapq

def a_star_search(grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    path_cost = {(start, None): 0}
    frontiers = [(heuristic(start, goal), start, None)]
    
    while frontiers:
        _, current, prev_dir = heapq.heappop(frontiers)

        if current == goal:
            return path_cost[current, prev_dir]

        for neighbor, new_dir, cost in get_neighbors(current, prev_dir, grid):
            c = path_cost[current, prev_dir] + cost
            if c < path_cost.get((neighbor, new_dir), 9e9):
                path_cost[neighbor, new_dir] = c
                heapq.heappush(frontiers, (c + heuristic(neighbor, goal), neighbor, new_dir))

def get_neighbors(cell, prev_dir, grid):
    if prev_dir is None:
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    else:
        dirs = [(prev_dir[1], -prev_dir[0]), (-prev_dir[1], prev_dir[0])]
        
    for di, dj in dirs:
        for k in range(MIN_STEPS, MAX_STEPS + 1):
            ni, nj = cell[0] + di * k, cell[1] + dj * k
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                cost = sum(grid[cell[0]+di*s][cell[1]+dj*s] for s in range(1, k+1))
                yield (ni, nj), (di, dj), cost
            else:
                break

def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


lines = read_input()
grid = [[int(c) for c in line] for line in lines]

MIN_STEPS = 1
MAX_STEPS = 3
print(a_star_search(grid))

MIN_STEPS = 4
MAX_STEPS = 10
print(a_star_search(grid))
