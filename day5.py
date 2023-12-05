# %%
from utils import *

seeds, *maps = read_lines(sep='\n\n')#, filename='day5-eg.txt')
seeds = list(map(int, seeds[6:].split()))
seeds

# %%
import re

def parse_maps(maps):
    ret = {}
    pat = r"(\w+)-to-(\w+) map:\n([\s\d]+)"
    for s in maps:
        m = re.match(pat, s)
        ret[m[1]] = (m[2], make_mapper(m[3].split('\n')))
    return ret

def make_mapper(lines):
    cases = []
    for line in lines:
        dst0, src0, n = map(int, line.split())
        cases.append([src0, src0+n, dst0-src0])
    return cases

def find_lowest_location(vals, maps):
    key = 'seed'
    while key != 'location':
        key, mapper = maps[key]
        for i, x in enumerate(vals):
            vals[i] = next((x + dx for x0, x1, dx in mapper if x0 <= x < x1), x)
    return min(vals)

print(find_lowest_location(seeds.copy(), parse_maps(maps)))

# %%
def find_intervals_lowest_location(intervals, maps):
    key = 'seed'
    while key != 'location':
        key, mapper = maps[key]
        mapped_intervals = []
        for lo, hi in intervals:
            for x0, x1, dx in mapper:
                int_lo = max(lo, x0)
                int_hi = min(hi, x1)
                if int_lo < int_hi:
                    mapped_intervals.append((int_lo + dx, int_hi + dx))
                    if int_lo > lo:
                        intervals.append((lo, int_lo))
                    if int_hi < hi:
                        intervals.append((int_hi, hi))
                    break
            else:
                mapped_intervals.append((lo, hi))
        intervals = mapped_intervals
    return min(lo for lo, hi in intervals)

intervals = [(lo, lo + n) for lo, n in zip(seeds[::2], seeds[1::2])]
print(find_intervals_lowest_location(intervals, parse_maps(maps)))
