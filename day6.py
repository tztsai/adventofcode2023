from utils import *
import re
import math

times, dists = read_lines()
# times, dists = """Time:      7  15   30
# Distance:  9  40  200""".splitlines()
records = list(zip(
    map(int, re.findall(r'\d+', times)),
    map(int, re.findall(r'\d+', dists))
))

# (T - t) * t > D
# t^2 - Tt + D < 0
# (T - sqrt(T^2 - 4D)) / 2 < t < (T + sqrt(T^2 - 4D)) / 2
def count_wins(T, D):
    lo = math.floor((T - math.sqrt(T**2 - 4*D)) / 2 + 1)
    hi = math.ceil((T + math.sqrt(T**2 - 4*D)) / 2 - 1)
    print(T, D, lo, hi)
    return hi - lo + 1

print(math.prod(count_wins(T, D) for T, D in records))

T = int(''.join(re.findall(r'\d+', times)))
D = int(''.join(re.findall(r'\d+', dists)))
print(count_wins(T, D))