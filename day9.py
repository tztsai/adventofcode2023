# %%
from utils import *
from itertools import islice, tee

seqs = [[int(n) for n in line.split()] for line in read_lines()]

def diff(seq):
    return [seq[i+1] - seq[i] for i in range(len(seq)-1)]

def get_next(seq):
    ds = diff(seq)
    if ds[0] == ds[-1] == 0:
        return seq[0]
    return seq[-1] + get_next(ds)

print(sum(get_next(seq) for seq in seqs))

# %%
def get_prev(seq):
    ds = diff(seq)
    if ds[0] == ds[-1] == 0:
        return seq[0]
    return seq[0] - get_prev(ds)

print(sum(get_prev(seq) for seq in seqs))
