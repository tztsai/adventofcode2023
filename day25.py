from utils import *
import numpy as np
import networkx as nx

def parse_graph(lines):
    g = {}
    for line in lines:
        a, b = line.split(': ')
        g[a] = b.split()
    return nx.Graph(g)

g = parse_graph(read_input())
fiddler = nx.fiedler_vector(g)
cluster1 = np.sum(fiddler < 0)
cluster2 = len(fiddler) - cluster1
print(cluster1 * cluster2)
