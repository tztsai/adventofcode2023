from utils import *

grids = read_input(sep='\n\n')
# grids = """#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#""".split('\n\n')
grids = list(map(str.splitlines, grids))

def find_mirror(grid, smudges=0):
    for k in range(1, len(grid)):
        if sum(diff(r1, r2) for r1, r2 in 
               zip(grid[k-1::-1], grid[k::])) == smudges:
            return (k, 0)
    return find_mirror(list(zip(*grid)), smudges)[::-1]

def diff(row1, row2):
    return sum(c1 != c2 for c1, c2 in zip(row1, row2))

print(sum(100*a + b for a, b in map(find_mirror, grids)))

print(sum(100*a + b for a, b in map(find_mirror, grids, [1] * len(grids))))
