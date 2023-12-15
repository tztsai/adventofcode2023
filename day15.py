from utils import *
from collections import defaultdict, OrderedDict

seq = read_lines()[0].split(',')
# seq = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(',')

def hash(s):
    h = 0
    for c in s:
        h = (h + ord(c)) * 17 & 0b11111111
    return h

print(sum(map(hash, seq)))

hashmap = defaultdict(OrderedDict)

for s in seq:
    if '=' in s:
        label, focal = s.split('=')
    else:
        label = s[:-1]
    box = hashmap[hash(label)]
    if '=' in s:
        box[label] = int(focal)
    else:
        box.pop(label, None)

print(sum((i+1) * (j+1) * f for i, box in hashmap.items() 
          for j, f in enumerate(box.values())))
