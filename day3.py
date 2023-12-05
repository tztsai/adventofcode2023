from utils import *

lines = read_lines()

import re
from itertools import product, chain
from collections import defaultdict
from math import prod

def scan(schematic):
    for i, line in enumerate(schematic):
        for m in re.finditer(r'\d+', line):
            for c, ii, jj in neighbors(schematic, i, m.start(), m.end()):
                if not c.isdigit() and c != '.':
                    yield int(m[0]), ii, jj
                    break

def neighbors(schematic, i, j1, j2):
    return ((schematic[ii][jj], ii, jj) for ii, jj 
            in chain(product([i-1, i+1], range(j1-1, j2+1)), [[i, j1-1], [i, j2]])
            if 0 <= ii < len(schematic) and 0 <= jj < len(schematic[0]))

print(sum(n for n, i, j in scan(lines)))

adj_nums = defaultdict(list)
for n, i, j in scan(lines):
    adj_nums[i, j].append(n)
print(sum(prod(ns) for ns in adj_nums.values() if len(ns) == 2))
