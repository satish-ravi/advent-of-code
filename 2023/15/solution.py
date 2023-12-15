import sys
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

def get_hash(string):
    hash_val = 0
    for ch in string:
        hash_val += ord(ch)
        hash_val *= 17
        hash_val %= 256
    return hash_val

@dataclass
class Operation:
    raw: str
    label: str

    @property
    def box(self):
        return get_hash(self.label)

@dataclass
class Delete(Operation):
    pass

@dataclass
class Assign(Operation):
    focal_length: int

@dataclass
class Lens:
    label: str
    focal_length: int

class Box:
    lenses: list

    def __init__(self):
        self.lenses = []

    def add_or_replace(self, label, focal_length):
        replaced = False
        for lens in self.lenses:
            if lens.label == label:
                lens.focal_length = focal_length
                replaced = True
                break
        if not replaced:
            self.lenses.append(Lens(label, focal_length))

    def remove(self, label):
        self.lenses = [lens for lens in self.lenses if lens.label != label]

    def get_power(self):
        return sum([(num + 1) * lens.focal_length for num, lens in enumerate(self.lenses)])

def parse_input(inp):
    operations = []
    for op in inp[0].split(','):
        if '-' in op:
            label = op.split('-')[0]
            operations.append(Delete(op, label))
        elif '=' in op:
            label, focal_length_str = op.split('=')
            operations.append(Assign(op, label, int(focal_length_str)))
        else:
            raise Exception(f'Invalid operation {op}')
    return operations

def part1(operations):
    return sum([get_hash(op.raw) for op in operations])

def part2(operations):
    boxes = [Box() for _ in range(256)]

    for operation in operations:
        if isinstance(operation, Assign):
            boxes[operation.box].add_or_replace(operation.label, operation.focal_length)
        else:
            boxes[operation.box].remove(operation.label)

    return sum([(num + 1) * box.get_power() for num, box in enumerate(boxes)])

operations = parse_input(inp)

print('part1:', part1(operations))
print('part2:', part2(operations))
