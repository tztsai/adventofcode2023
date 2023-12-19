from utils import *

instr, _, *lines = read_input()

graph = {
    m[0]: (m[1], m[2])
    for line in lines
    for m in re.findall(r'(\w+) = \((\w+), (\w+)\)', line)
}

instr = list(map('LR'.index, instr))

def walk(graph, instr, start='AAA', end='ZZZ'):
    node = start
    for i, d in enumerate(instr):
        node = graph[node][d]
        if callable(end) and end(node):
            return i + 1
        if node == end:
            return i + 1
    return len(instr) + walk(graph, instr, node, end)

print(walk(graph, instr))

def find_cycle(graph, instr, node):
    steps = 0
    node1 = node2 = node
    def step():
        nonlocal steps, node1, node2
        node1 = graph[node1][instr[steps % len(instr)]]
        node2 = graph[node2][instr[(steps*2) % len(instr)]]
        node2 = graph[node2][instr[(steps*2+1) % len(instr)]]
        steps += 1
    step()
    while node1 != node2 or steps % len(instr) != (steps*2) % len(instr):
        step()
        if node1.endswith('Z') or node2.endswith('Z'):
            assert node1 == node2 and steps % len(instr) == 0
            # there is only **Z node in the cycle and it's at the end!
    return steps

def parallel_walks(graph, instr):
    nodes = [n for n in graph if n.endswith('A')]
    lens = [find_cycle(graph, instr, n) for n in nodes]
    return math.lcm(*lens)
    # steps = 0
    # while not all(n.endswith('Z') for n in nodes):
    #     d = instr[steps % len(instr)]
    #     nodes = [graph[n][d] for n in nodes]
    #     steps += 1
    # return steps

print(parallel_walks(graph, instr))
