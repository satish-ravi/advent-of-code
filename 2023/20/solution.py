import sys
from collections import deque
from dataclasses import dataclass
from enum import Enum
import math
inp = list(l.strip() for l in sys.stdin.readlines())

class Pulse(Enum):
    low = 'low'
    high = 'high'

@dataclass
class Module:
    name: str
    destinations: list[str]

    def get_next(self, pulse):
        return [(destination, pulse, self.name) for destination in self.destinations]

    def process(self, pulse, source):
        return self.get_next(pulse)

    def reset(self):
        pass

@dataclass
class FlipFlop(Module):
    state: bool = False

    def process(self, pulse, source):
        if pulse == Pulse.high:
            return []
        next_pulse = Pulse.low if self.state else Pulse.high
        self.state = not self.state
        return self.get_next(next_pulse)

    def reset(self):
        self.state = False

@dataclass
class Conjunction(Module):
    input_memory: dict[str, Pulse]

    def process(self, pulse, source):
        self.input_memory[source] = pulse
        return self.get_next(Pulse.low if all(inp_pulse == Pulse.high for inp_pulse in self.input_memory.values()) else Pulse.high)

    def reset(self):
        for module in self.input_memory.keys():
            self.input_memory[module] = Pulse.low

def parse_input(inp):
    modules = {}
    conjunction_names = set([])
    for row in inp:
        module, dest = row.split(' -> ')
        if module[0] == '%':
            modules[module[1:]] = FlipFlop(module[1:], dest.split(', '))
        elif module[0] == '&':
            modules[module[1:]] = Conjunction(module[1:], dest.split(', '), {})
            conjunction_names.add(module[1:])
        else:
            modules['broadcaster'] = Module('broadcaster', dest.split(', '))

    for module_name, module in modules.items():
        for dest in module.destinations:
            if dest in conjunction_names:
                modules[dest].input_memory[module_name] = Pulse.low

    return modules

def run_cycle(modules):
    pulse_counts = {
        Pulse.low: 0,
        Pulse.high: 0
    }
    q = deque([('broadcaster', Pulse.low, 'button')])
    low_pulse_modules = set([])

    while q:
        module, pulse, source = q.popleft()
        pulse_counts[pulse] += 1

        if pulse == Pulse.low:
            low_pulse_modules.add(module)

        if module in modules:
            q.extend(modules[module].process(pulse, source))

    return pulse_counts, low_pulse_modules

def lcm_of_list(numbers):
    if len(numbers) == 0:
        raise ValueError("List must contain at least one number.")

    result = numbers[0]

    for num in numbers[1:]:
        result = abs(result * num) // math.gcd(result, num)

    return result

def part1(modules):
    pulse_counts = {
        Pulse.low: 0,
        Pulse.high: 0
    }
    for _ in range(1000):
        cycle_counts, _ = run_cycle(modules)
        pulse_counts[Pulse.low] += cycle_counts[Pulse.low]
        pulse_counts[Pulse.high] += cycle_counts[Pulse.high]
    return pulse_counts[Pulse.low] * pulse_counts[Pulse.high]

def part2(modules):
    for module in modules.values():
        module.reset()

    rx_in = [module_name for module_name, module in modules.items() if module.destinations == ['rx']][0]
    modules_to_track = {module_name: None for module_name in modules[rx_in].input_memory.keys()}

    buttons_pressed = 0
    while any(count == None for count in modules_to_track.values()):
        buttons_pressed += 1

        _, low_pulse_modules = run_cycle(modules)

        for module_to_track, press_count in modules_to_track.items():
            if not press_count and module_to_track in low_pulse_modules:
                modules_to_track[module_to_track] = buttons_pressed

    return lcm_of_list(list(modules_to_track.values()))


modules = parse_input(inp)

print('part1:', part1(modules))
print('part2:', part2(modules))
