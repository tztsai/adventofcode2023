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

    def connect(self, other):
        self.channels_out.append(other)
        other.connect_in(self)
        
    def connect_in(self, other):
        self.channels_in.append(other)
    
    def forward(self, value: int, source: str):
        # print(f"{source} -{value}-> {self.name}")
        Module.global_counter[value] += 1
        if (out := self(value, source)) is not None:
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
    channels = [[modules.get(ch, Module(ch)) for ch in pair]
                for pair in channels]
    graph = nx.DiGraph()
    graph.add_edges_from(channels)
    for chan_in, chan_out in channels:
        chan_in.connect(chan_out)
    return modules, graph

lines = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()
lines = read_input()

network, graph = build_network(lines)
graph = nx.nx_pydot.write_dot(graph, 'graph.dot')

# for _ in range(1000):
#     Module.send(network['broadcaster'], 0)
# print(math.prod(Module.global_counter))

def monitor_presses(klass, label):
    counter = [0, 0]
    presses = 0
    
    def forward(self, value, source):
        if self.name == label:
            counter[value] += 1
        return _forward(self, value, source)
    
    _forward = klass.forward
    klass.forward = forward
    states = {}
    traces = defaultdict(list)
    cycles = {}
    
    while True:
        klass.send(network['br'], 0)
        presses += 1
        if counter[0] == 1:
            return presses
        s = get_state(network)
        for k, v in s:
            traces[k].append(v)
        if presses < 10000:
            continue
        for k, t in traces.items():
            if cycles.get(k, 0) < (cycle := detect_cycle(t)):
                cycles[k] = cycle
                print(k, cycle, t[:cycle])
        counter = [0, 0]

def detect_cycle(trace):
    i = 1
    trace = trace[::-1]
    while i <= len(trace) // 10:
        if all(trace[k*i:(k+1)*i] == trace[(k+1)*i:(k+2)*i] for k in range(10)):
            return i
        i += 1
    return 0

def get_state(network):
    return tuple((k, v.state) for k, v in network.items() if isinstance(v, FlipFlop))

print(monitor_presses(Module, 'rx'))

"""
strict digraph  {
"FlipFlop(fg)";
"Conjunction(nt)";
"FlipFlop(gt)";
"Conjunction(zp)";
"Module(rx)";
"FlipFlop(fh)";
"FlipFlop(xz)";
"FlipFlop(pj)";
"FlipFlop(zj)";
"Conjunction(zq)"; 
"FlipFlop(jc)";
"FlipFlop(nk)";
"FlipFlop(mr)";
"Conjunction(vv)";
"FlipFlop(pz)";
"FlipFlop(cl)";
"FlipFlop(fp)";
"FlipFlop(xb)";
"FlipFlop(bl)";
"FlipFlop(nc)";
"FlipFlop(mg)";
"Conjunction(vn)";
"FlipFlop(cf)";
"Conjunction(sb)";
"FlipFlop(ht)";
"FlipFlop(pp)";
"FlipFlop(rq)";
"FlipFlop(ft)";
"Conjunction(nd)";
"FlipFlop(ps)";
"FlipFlop(xm)";
"FlipFlop(fs)";
"FlipFlop(ff)";
"FlipFlop(nb)";
"FlipFlop(dv)";
"FlipFlop(qd)";
"FlipFlop(kg)";
"FlipFlop(hr)";
"FlipFlop(rm)";
"FlipFlop(dm)";
"FlipFlop(mq)";
"FlipFlop(br)";
"FlipFlop(jz)";
"FlipFlop(gr)";
"FlipFlop(ln)";
"FlipFlop(bh)";
"FlipFlop(zc)";
"FlipFlop(zv)";
"FlipFlop(dc)";
"FlipFlop(qs)";
"FlipFlop(rd)";
"Conjunction(ds)";
"FlipFlop(bb)";
"FlipFlop(qn)";
"FlipFlop(lm)";
"FlipFlop(dr)";
"FlipFlop(xd)";
"Conjunction(hf)";
"Broadcaster(broadcaster)";
"FlipFlop(fg)" -> "Conjunction(nt)";
"FlipFlop(fg)" -> "FlipFlop(gt)";
"Conjunction(nt)" -> "FlipFlop(rq)";
"Conjunction(nt)" -> "FlipFlop(fg)";
"Conjunction(nt)" -> "FlipFlop(ft)";
"Conjunction(nt)" -> "Conjunction(nd)";
"Conjunction(nt)" -> "FlipFlop(gt)";
"Conjunction(nt)" -> "FlipFlop(xz)";
"FlipFlop(gt)" -> "FlipFlop(jc)";
"Conjunction(zp)" -> "Module(rx)";
"FlipFlop(fh)" -> "Conjunction(nt)";
"FlipFlop(fh)" -> "FlipFlop(xz)";
"FlipFlop(xz)" -> "FlipFlop(dr)";
"FlipFlop(pj)" -> "FlipFlop(zj)";
"FlipFlop(pj)" -> "Conjunction(zq)";
"FlipFlop(zj)" -> "FlipFlop(cf)";
"Conjunction(zq)" -> "FlipFlop(fs)";
"Conjunction(zq)" -> "FlipFlop(gr)";
"Conjunction(zq)" -> "FlipFlop(ff)";
"Conjunction(zq)" -> "Conjunction(hf)";
"Conjunction(zq)" -> "FlipFlop(ln)";
"Conjunction(zq)" -> "FlipFlop(zj)";
"Conjunction(zq)" -> "FlipFlop(pj)";
"FlipFlop(jc)" -> "Conjunction(nt)";
"FlipFlop(jc)" -> "FlipFlop(nk)";
"FlipFlop(nk)" -> "FlipFlop(rq)";
"FlipFlop(nk)" -> "Conjunction(nt)";
"FlipFlop(mr)" -> "Conjunction(vv)";
"FlipFlop(mr)" -> "FlipFlop(pz)";
"Conjunction(vv)" -> "FlipFlop(dm)";
"Conjunction(vv)" -> "FlipFlop(bl)";
"Conjunction(vv)" -> "Conjunction(sb)";
"Conjunction(vv)" -> "FlipFlop(nb)";
"Conjunction(vv)" -> "FlipFlop(qd)";
"Conjunction(vv)" -> "FlipFlop(bh)";
"FlipFlop(pz)" -> "Conjunction(vv)";
"FlipFlop(cl)" -> "FlipFlop(fp)";
"FlipFlop(cl)" -> "Conjunction(zq)";
"FlipFlop(fp)" -> "FlipFlop(rd)";
"FlipFlop(fp)" -> "Conjunction(zq)";
"FlipFlop(xb)" -> "FlipFlop(bl)";
"FlipFlop(xb)" -> "Conjunction(vv)";
"FlipFlop(bl)" -> "FlipFlop(bb)";
"FlipFlop(nc)" -> "Conjunction(zq)";
"FlipFlop(mg)" -> "Conjunction(vn)";
"Conjunction(vn)" -> "FlipFlop(br)";
"Conjunction(vn)" -> "FlipFlop(jz)";
"Conjunction(vn)" -> "FlipFlop(ht)";
"Conjunction(vn)" -> "FlipFlop(ps)";
"Conjunction(vn)" -> "FlipFlop(zc)";
"Conjunction(vn)" -> "FlipFlop(pp)";
"Conjunction(vn)" -> "Conjunction(ds)";
"FlipFlop(cf)" -> "FlipFlop(gr)";
"FlipFlop(cf)" -> "Conjunction(zq)";
"Conjunction(sb)" -> "Conjunction(zp)";
"FlipFlop(ht)" -> "FlipFlop(pp)";
"FlipFlop(pp)" -> "FlipFlop(mq)";
"FlipFlop(rq)" -> "FlipFlop(ft)";
"FlipFlop(ft)" -> "FlipFlop(fh)";
"Conjunction(nd)" -> "Conjunction(zp)";
"FlipFlop(ps)" -> "FlipFlop(xm)";
"FlipFlop(xm)" -> "Conjunction(vn)";
"FlipFlop(xm)" -> "FlipFlop(ht)";
"FlipFlop(fs)" -> "FlipFlop(ff)";
"FlipFlop(ff)" -> "FlipFlop(cl)";
"FlipFlop(nb)" -> "FlipFlop(dv)";
"FlipFlop(dv)" -> "Conjunction(vv)";
"FlipFlop(dv)" -> "FlipFlop(hr)";
"FlipFlop(qd)" -> "FlipFlop(xb)";
"FlipFlop(kg)" -> "FlipFlop(mr)";
"FlipFlop(kg)" -> "Conjunction(vv)";
"FlipFlop(hr)" -> "FlipFlop(dm)";
"FlipFlop(hr)" -> "Conjunction(vv)";
"FlipFlop(rm)" -> "Conjunction(zq)";
"FlipFlop(rm)" -> "FlipFlop(fs)";
"FlipFlop(dm)" -> "FlipFlop(kg)";
"FlipFlop(mq)" -> "Conjunction(vn)";
"FlipFlop(mq)" -> "FlipFlop(zc)";
"FlipFlop(br)" -> "Conjunction(vn)";
"FlipFlop(br)" -> "FlipFlop(jz)";
"FlipFlop(jz)" -> "FlipFlop(qs)";
"FlipFlop(gr)" -> "FlipFlop(ln)";
"FlipFlop(ln)" -> "FlipFlop(rm)";
"FlipFlop(bh)" -> "FlipFlop(qd)";
"FlipFlop(bh)" -> "Conjunction(vv)";
"FlipFlop(zc)" -> "FlipFlop(zv)";
"FlipFlop(zv)" -> "FlipFlop(dc)";
"FlipFlop(zv)" -> "Conjunction(vn)";
"FlipFlop(dc)" -> "FlipFlop(mg)";
"FlipFlop(dc)" -> "Conjunction(vn)";
"FlipFlop(qs)" -> "Conjunction(vn)";
"FlipFlop(qs)" -> "FlipFlop(ps)";
"FlipFlop(rd)" -> "FlipFlop(nc)";
"FlipFlop(rd)" -> "Conjunction(zq)";
"Conjunction(ds)" -> "Conjunction(zp)";
"FlipFlop(bb)" -> "FlipFlop(nb)";
"FlipFlop(bb)" -> "Conjunction(vv)";
"FlipFlop(qn)" -> "Conjunction(nt)";
"FlipFlop(lm)" -> "Conjunction(nt)";
"FlipFlop(lm)" -> "FlipFlop(qn)";
"FlipFlop(dr)" -> "FlipFlop(xd)";
"FlipFlop(dr)" -> "Conjunction(nt)";
"FlipFlop(xd)" -> "Conjunction(nt)";
"FlipFlop(xd)" -> "FlipFlop(lm)";
"Conjunction(hf)" -> "Conjunction(zp)";
"Broadcaster(broadcaster)" -> "FlipFlop(pj)";
"Broadcaster(broadcaster)" -> "FlipFlop(fg)";
"Broadcaster(broadcaster)" -> "FlipFlop(bh)";
"Broadcaster(broadcaster)" -> "FlipFlop(br)";
}
"""