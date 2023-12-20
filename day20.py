from utils import *
from collections import deque, defaultdict
import networkx as nx

class Module:
    global_counter = [0, 0]
    global_queue = deque()

    def __init__(self, name):
        self.name = name
        self.channels_in = []
        self.channels_out = []
        self.state = None
        self.counter = [0, 0]

    def connect(self, other):
        self.channels_out.append(other)
        other.connect_in(self)
        
    def connect_in(self, other):
        self.channels_in.append(other)
    
    def forward(self, value: int, source: str):
        # print(f"{source} -{value}-> {self.name}")
        Module.global_counter[value] += 1
        if (out := self(value, source)) is not None:
            self.counter[out] += 1
            for ch in self.channels_out:
                Module.global_queue.append((ch, out, self.name))

    def __call__(self, value, source):
        return None
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name})"#"[{','.join(m.name for m in self.channels_out)}]"

    @classmethod
    def send(cls, module, input, source='button'):
        module.forward(input, source)
        while cls.global_queue:
            cls.forward(*cls.global_queue.popleft())

class Broadcaster(Module):
    def __call__(self, value, _):
        return value

class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = 0

    def __call__(self, value, _):
        if value == 0:
            self.state = 1 - self.state
            return self.state
        
class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = {}
        
    def connect_in(self, other):
        super().connect_in(other)
        self.state[other.name] = 0
    
    def __call__(self, value, source):
        self.state[source] = value
        return 1 - int(all(self.state.values()))

def parse_module(line):
    name, outputs = line.split(' -> ')
    match name[0]:
        case 'b':
            klass = Broadcaster
        case '%':
            klass = FlipFlop
            name = name[1:]
        case '&':
            klass = Conjunction
            name = name[1:]
        case _:
            raise ValueError(f"Unknown module type: {name[0]}")
    channels_out = outputs.split(', ')
    return klass(name), channels_out

def build_network(lines):
    modules = {}
    channels = []
    
    for line in lines:
        chan_in, chans_out = parse_module(line)
        modules[chan_in.name] = chan_in
        for name_out in chans_out:
            channels.append((chan_in.name, name_out))

    channels = [[modules.get(ch, Module(ch)) for ch in pair] for pair in channels]
    for chan_in, chan_out in channels:
        chan_in.connect(chan_out)

    graph = nx.DiGraph()
    graph.add_edges_from(channels)
    nx.nx_pydot.write_dot(graph, 'circuit.dot')
    
    return modules

lines = read_input()

network = build_network(lines)

for _ in range(1000):
    Module.send(network['broadcaster'], 0)
print(math.prod(Module.global_counter))

def monitor_presses(network, entry='broadcaster'):
    first_flips = {}
    traces = defaultdict(list)
    presses = 0
    diffs = set()
    conj = next(m for m in network[entry].channels_out if isinstance(m, Conjunction))
    
    for _ in range(10000):
        Module.send(network[entry], 0)
        presses += 1
        if set(first_flips) == set(network):
            return presses
        for k, m in network.items():
            if isinstance(m, FlipFlop):
                traces[k].append(m.state)
                if m.state and k not in first_flips:
                    first_flips[k] = presses
        state = ''.join(
            str(traces[k][-1]) for k, _ in
            sorted(first_flips.items(), key=lambda t: t[1]))[::-1]
        if (d := presses - int(state, 2)) not in diffs:
            diffs.add(d)
            print(presses, conj.counter[0], diffs)
    
    diffs = sorted(diffs)
    assert all(diffs[i] - diffs[i-1] == diffs[1] for i in range(2, len(diffs)))
    conj_in_flips = [first_flips[m.name] for m in conj.channels_out if isinstance(m, FlipFlop)]
    # print(sum(conj_in_flips) + diffs[1])
    return diffs[1]

ans = 1
for m in network['broadcaster'].channels_out:
    network = build_network(lines)
    p = monitor_presses(network, m.name)
    ans *= p
    
print(ans)