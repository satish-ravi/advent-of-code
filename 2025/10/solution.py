import sys
from dataclasses import dataclass
from collections import deque
import z3

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass
class Machine:
    lights: list[bool]
    buttons: list[list[int]]
    joltage: list[int]

def parse_input(inp):
    machines = []
    for line in inp:
        split = line.split(' ')
        lights = [b == '#' for b in split[0][1:-1]]
        joltage = [int(j) for j in split[-1][1:-1].split(',')]
        buttons = [[int(b) for b in button[1:-1].split(',')] for button in split[1:-1]]
        machines.append(Machine(lights, buttons, joltage))
    return machines


def get_min_steps_to_turn_on_lights(machine):
    initial = [False] * len(machine.lights)
    q = deque([(initial, 0)])
    visited = set([tuple(initial)])

    while q:
        lights, steps = q.popleft()
        if lights == machine.lights:
            return steps
        for button in machine.buttons:
            new_lights = lights[:]
            for b in button:
                new_lights[b] = not new_lights[b]
            if tuple(new_lights) not in visited:
                visited.add(tuple(new_lights))
                q.append((new_lights, steps + 1))
    return None

def get_min_steps_to_joltage(machine):
    solver = z3.Optimize()
    buttons = [z3.Int(f'button_{i}') for i in range(len(machine.buttons))]
    solver.add(z3.And(*[buttons[i] >= 0 for i in range(len(machine.buttons))]))
    for i, joltage in enumerate(machine.joltage):
        solver.add(sum(buttons[j] for j, button in enumerate(machine.buttons) if i in button) == joltage)

    solver.minimize(sum(buttons))
    solver.check()
    model = solver.model()
    res = 0
    for b in buttons:
        res += model[b].as_long()
    return res

def part1(machines):
    return sum(get_min_steps_to_turn_on_lights(machine) for machine in machines)

def part2(machines):
    return sum(get_min_steps_to_joltage(machine) for machine in machines)

machines = parse_input(inp)
print('part1:', part1(machines))
print('part2:', part2(machines))
