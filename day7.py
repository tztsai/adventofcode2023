# %%
from utils import *
from collections import Counter

lines = read_input()
# lines = '''32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483'''.splitlines()

hands, bids = zip(*map(str.split, lines))
card_stren = {c: i for i, c in enumerate('23456789TJQKA')}

def rank(i, hands=hands):
    hand = hands[i]
    c = Counter(hand)
    s = tuple(map(card_stren.get, hand))
    return (max(c.values()), -len(c), s)

ids_by_rank = sorted(range(len(hands)), key=rank)
print(sum(int(bids[i]) * (r+1) for r, i in enumerate(ids_by_rank)))

# %%
card_stren = {c: i for i, c in enumerate('J23456789TQKA')}

def new_rank(i, hands=hands):
    hand = list(hands[i])
    c = Counter(hand)
    s = tuple(map(card_stren.get, hand))  # J does not change for tie-breaking
    if 'J' in hand:
        best_card = max(((c[n], card_stren[n], n) for n in hand
                        if n != 'J'), default='A')[-1]
        hand = [n if n != 'J' else best_card for n in hand]
        c[best_card] += c.pop('J')
    return (max(c.values()), -len(c), s)

ids_by_rank = sorted(range(len(hands)), key=new_rank)
print(sum(int(bids[i]) * (r+1) for r, i in enumerate(ids_by_rank)))

# %%
