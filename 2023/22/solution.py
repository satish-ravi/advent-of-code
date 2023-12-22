import sys
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    @classmethod
    def get_point(cls, pt_str):
        x, y, z = pt_str.split(',')
        return Point(int(x), int(y), int(z))

    def __repr__(self):
        return f'{self.x},{self.y},{self.z}'

@dataclass(frozen=True)
class Brick:
    p1: Point
    p2: Point

    @property
    def low_z(self):
        return min(self.p1.z, self.p2.z)

    @property
    def high_z(self):
        return max(self.p1.z, self.p2.z)

    def x_range(self):
        return range(min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x) + 1)

    def y_range(self):
        return range(min(self.p1.y, self.p2.y), max(self.p1.y, self.p2.y) + 1)

    def z_range(self):
        return range(min(self.p1.z, self.p2.z), max(self.p1.z, self.p2.z) + 1)

    def get_all_points(self):
        pts = []
        for x in self.x_range():
            for y in self.y_range():
                for z in self.z_range():
                    pts.append(Point(x, y, z))
        return set(pts)

    def get_lowered(self, z):
        if z == self.low_z:
            return self
        return Brick(Point(self.p1.x, self.p1.y, self.p1.z - self.low_z + z), Point(self.p2.x, self.p2.y, self.p2.z - self.low_z + z))

    def __repr__(self):
        return f'{self.p1}~{self.p2}'

def parse_input(inp):
    bricks = []
    for row in inp:
        p1, p2 = row.split('~')
        bricks.append(Brick(Point.get_point(p1), Point.get_point(p2)))
    return bricks

def simulate(bricks):
    occupied = {}
    fallen_bricks = []
    for brick in sorted(bricks, key=lambda b: b.low_z):
        z = brick.low_z
        stop = False
        while z > 1:
            for x in brick.x_range():
                for y in brick.y_range():
                    if Point(x, y, z - 1) in occupied:
                        stop = True
                        break
                if stop:
                    break
            if stop:
                break
            z -= 1
        fallen_brick = brick.get_lowered(z)
        fallen_bricks.append(fallen_brick)

        for point in fallen_brick.get_all_points():
            occupied[point] = fallen_brick

    above = {b: set([]) for b in fallen_bricks}
    below = {b: set([]) for b in fallen_bricks}

    for brick in fallen_bricks:
        for x in brick.x_range():
            for y in brick.y_range():
                above_point = Point(x, y, brick.high_z + 1)
                if above_point in occupied:
                    above[brick].add(occupied[above_point])
                below_point = Point(x, y, brick.low_z - 1)
                if below_point in occupied:
                    below[brick].add(occupied[below_point])

    return fallen_bricks, above, below

def part1(fallen_bricks, above, below):
    result = 0
    for brick in fallen_bricks:
        if all(len(below[above_brick]) != 1 for above_brick in above[brick]):
            result += 1
    return result

def part2(fallen_bricks, above, below):
    result = 0

    for brick in fallen_bricks:
        removed = set([brick])
        new_removed = True
        while new_removed:
            new_removed = False
            for removed_brick in list(removed):
                for above_brick in above[removed_brick]:
                    if not above_brick in removed and len(below[above_brick] - removed) == 0:
                        removed.add(above_brick)
                        new_removed = True
        result += len(removed) - 1
    return result

bricks = parse_input(inp)
fallen_bricks, above, below = simulate(bricks)
print('part1:', part1(fallen_bricks, above, below))
print('part2:', part2(fallen_bricks, above, below))
