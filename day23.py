from utils import *
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

grid = read_input()
start = (0, grid[0].index('.'))
goal = (len(grid) - 1, grid[-1].index('.'))

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
slope_dirs = dict(zip('>v<^', [[d] for d in dirs]))

def get_neighbors(i, j, grid):
    for di, dj in slope_dirs.get(grid[i][j], dirs):
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
            if grid[ni][nj] != '#':
                yield (ni, nj), 1

def to_graph(grid):
    return {(i, j): dict(get_neighbors(i, j, grid))
            for i, row in enumerate(grid)
            for j, c in enumerate(row) if c != '#'}

def compress_graph(graph, start, goal):
    """Compresses a graph by removing nodes with only two neighbors."""
    key_nodes = set(n for n, nbs in graph.items()
                    if len(nbs) > 2 or n in (start, goal))
    new_graph = defaultdict(dict)
    
    def get_neighbors(node):
        for nb, dist in graph[node].items():
            prev = node
            try:
                while nb not in key_nodes:
                    n, d = next(it for it in graph[nb].items() if it[0] != prev)
                    nb, prev = n, nb
                    dist += d
            except StopIteration:
                continue
            yield nb, dist
    
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for n, d in get_neighbors(node):
            new_graph[node][n] = d
            stack.append(n)

    return new_graph

def search_longest_path(graph, start, goal):
    visited = set()
    
    def dfs(node, length):
        if node == goal:
            return length
        visited.add(node)
        res = max([dfs(n, length + d) for n, d in graph[node].items()
                   if n not in visited], default=-1)
        visited.remove(node)
        return res

    return dfs(start, 0)

graph = compress_graph(to_graph(grid), start, goal)
print(graph)

print(search_longest_path(graph, start, goal))

slope_dirs = dict(zip('>v<^', [dirs] * 4))
graph = compress_graph(to_graph(grid), start, goal)
print(graph)

G = nx.Graph()
G.add_weighted_edges_from([(n, n2, d) for n, nbs in graph.items() for n2, d in nbs.items()])
nx.draw(G, with_labels=True, node_size=1500, font_size=10)
plt.show()

print(search_longest_path(graph, start, goal))
