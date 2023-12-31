from utils import *

grid = tuple(read_input())
# grid = """O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....""".splitlines()

def tilt_horizontal(grid, direction=-1):
    return tuple(
        '#'.join(''.join(sorted(p, reverse=direction < 0))
                 for p in row.split('#'))
        for row in grid
    )  # e.g. '.O..OO.' is sorted to 'OOO....'

def tilt_vertical(grid, direction=-1):
    grid_T = map(''.join, zip(*grid))
    return tuple(map(''.join, zip(*tilt_horizontal(grid_T, direction))))

def calc_load(grid):
    return sum((len(grid)-i) * row.count('O') for i, row in enumerate(grid))

print(calc_load(tilt_vertical(grid, -1)))

def tilt_cycle(grid):
    grid = tilt_vertical(grid, -1)
    grid = tilt_horizontal(grid, -1)
    grid = tilt_vertical(grid, 1)
    grid = tilt_horizontal(grid, 1)
    return grid

i = 0
cache = {grid: 0}

while i < 1000000000:
    grid = tilt_cycle(grid)
    i += 1
    if 'cycle_len' in globals():
        continue
    elif grid in cache:
        cycle_start = cache[grid]
        cycle_len = i - cycle_start
        print("cycle start:", cycle_start, "cycle len:", cycle_len)
        i += ((1000000000 - i) // cycle_len) * cycle_len
    else:
        cache[grid] = i

print(calc_load(grid))