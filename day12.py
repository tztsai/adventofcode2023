from utils import *
from functools import lru_cache
from tqdm import tqdm
import tracemalloc

lines = read_lines()
# lines = """???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1""".splitlines()

inputs = [(r, tuple(map(int, g.split(','))))
          for r, g in map(str.split, lines)]

@lru_cache(2 ** 20)
def count_arranges(row, groups):
    row = row.strip('.')
    if len(row) < sum(groups):
        return 0
    if not groups:
        return int('#' not in row)
    if '.' in row:
        left, right = re.split(r'\.+', row, 1)
        return sum(count_arranges(left, groups[:i]) * 
                   count_arranges(right, groups[i:])
                   for i in range(0, len(groups)+1))
    n = 0
    if len(row) == groups[0] or row[groups[0]] != '#':
        n += count_arranges(row[groups[0]+1:], groups[1:])
    if row[0] != '#':
        n += count_arranges(row[1:], groups)
    return n

print(sum(count_arranges(r, g) for r, g in inputs))

def count_unfolded_arranges(rows, groups, k=5):
    return count_arranges('?'.join([rows] * k), groups * k)

tracemalloc.start()

print(sum(count_unfolded_arranges(r, g) for r, g in tqdm(inputs)))

print("Current {:.2f} MB, Peak {:.2f} MB"
      .format(*map(lambda x: x / 10**6, tracemalloc.get_traced_memory())))