from utils import *
from collections import deque

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
        return f"{type(self).__name__}({self.name})[{','.join(m.name for m in self.channels_out)}]"

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
        module, channels_out = parse_module(line)
        modules[module.name] = module
        for ch_out in channels_out:
            channels.append((module, ch_out))
    for module, ch_out in channels:
        if ch_out not in modules:
            modules[ch_out] = Module(ch_out)
        module.connect(modules[ch_out])
    return modules

lines = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()
lines = read_input()

network = build_network(lines)

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
    
    while True:
        klass.send(network['broadcaster'], 0)
        presses += 1
        if counter[0] == 1:
            return presses
        # s = get_state(network)
        # print(''.join(str(v) for k, v in s))
        # if s in states:
        #     return presses, states[s]
        # states[s] = presses
        # if any(network['zp'].state.values()):
        #     print(presses, network['zp'].state, counter)
        counter = [0, 0]

def get_state(network):
    return tuple((k, v.state) for k, v in network.items() if isinstance(v, FlipFlop))

print(monitor_presses(Module, 'rx'))
