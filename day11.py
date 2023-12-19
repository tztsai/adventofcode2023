from utils import *

lines = read_input()

galaxies = [
    (i, j) for i, row in enumerate(lines)
    for j, char in enumerate(row) if char == '#'
]

def expand(poses, axis, scale=2):
    rs = sorted(set(p[axis] for p in poses))
    new_rs = []
    for i in range(len(rs)):
        r = rs[i]
        r0 = rs[i - 1] if i > 0 else -1
        new_r0 = new_rs[-1] if new_rs else -1
        new_rs.append(new_r0 + 1 + (r - r0 - 1) * scale)
    return dict(zip(rs, new_rs))

def shortest_path_len(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

expand_row = expand(galaxies, 0)
expand_col = expand(galaxies, 1)

galaxies1 = [
    (expand_row[i], expand_col[j]) for i, j in galaxies
]

print(sum(shortest_path_len(galaxies1[i], galaxies1[j])
          for i in range(len(galaxies1)) for j in range(i)))

expand_row = expand(galaxies, 0, 1000000)
expand_col = expand(galaxies, 1, 1000000)

galaxies2 = [
    (expand_row[i], expand_col[j]) for i, j in galaxies
]

print(sum(shortest_path_len(galaxies2[i], galaxies2[j])
            for i in range(len(galaxies2)) for j in range(i)))