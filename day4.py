from utils import *
from collections import Counter

lines = read_lines()

def matches(game):
    pattern = r"Card\s+\d+:\s+((?:\d+\s+)+)\|((?:\s+\d+)+)"
    a, b = [set(map(int, part.split())) for part in re.match(pattern, game).groups()]
    return len(a & b)

def score(game):
    m = matches(game)
    return m and 2 ** (m - 1)

print(sum(score(game) for game in lines))

def grow_cards(games):
    counts = Counter(range(len(games)))
    for i, game in enumerate(games):
        counts.update({j: counts[i] for j in range(i+1, i+matches(game)+1) if j < len(games)})
    return sum(counts.values())

print(grow_cards(lines))