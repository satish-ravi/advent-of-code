import sys
from dataclasses import dataclass
inp = sys.stdin.read()

@dataclass
class Shape:
    id: int
    points: list[tuple[int, int]]

    @classmethod
    def from_string(cls, string):
        id, raw_points = string.split(':\n')
        id = int(id)
        points = []
        for r, row in enumerate(raw_points.split('\n')):
            for c, point in enumerate(row):
                if point == '#':
                    points.append((r, c))
        return cls(id, points)

@dataclass
class Region:
    rows: int
    cols: int
    shape_counts: list[int]

    @classmethod
    def from_string(cls, string):
        rowcol, shape_counts = string.split(': ')
        rows, cols = rowcol.split('x')
        rows = int(rows)
        cols = int(cols)
        shape_counts = [int(count) for count in shape_counts.split(' ')]
        return cls(rows, cols, shape_counts)

def parse_input(inp):
    *shapes, regions = inp.split('\n\n')
    shapes = [Shape.from_string(shape) for shape in shapes]
    regions = [Region.from_string(region) for region in regions.split('\n')]
    return shapes, regions

def part1(shapes, regions):
    ans = 0
    for region in regions:
        required_total = 0
        for i in range(len(region.shape_counts)):
            required_total += region.shape_counts[i] * len(shapes[i].points)
        if required_total <= region.rows * region.cols:
            ans += 1
    return ans

shapes, regions = parse_input(inp)
print('part1:', part1(shapes, regions))
