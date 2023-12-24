import sys
import z3
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

ranges = (200000000000000, 400000000000000)
ranges_test = (7, 27)

@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @property
    def m(self):
        return self.vy / self.vx

    @property
    def b(self):
        return self.y - self.m * self.x

    def t_at(self, x):
        return (x - self.x) / self.vx


def parse_input(inp):
    stones = []
    for row in inp:
        p, v = row.split(' @ ')
        x, y, z = p.split(', ')
        vx, vy, vz = v.split(', ')
        stones.append(Hailstone(int(x), int(y), int(z), int(vx), int(vy), int(vz)))
    return stones


def part1(stones):
    result = 0
    for i in range(len(stones) - 1):
        for j in range(i+1, len(stones)):
            mi, mj = stones[i].m, stones[j].m
            bi, bj = stones[i].b, stones[j].b
            if mi == mj:
                if bi == bj:
                    result += 1
                continue
            x = (bj - bi) / (mi - mj)
            y = mi * x + bi
            ti = stones[i].t_at(x)
            tj = stones[j].t_at(x)
            lower, upper = ranges
            if lower <= x <= upper and lower <= y <= upper and ti >= 0 and tj >= 0:
                result += 1
    return result

def part2(stones):
    x = z3.Real('x')
    y = z3.Real('y')
    z = z3.Real('z')
    vx = z3.Real('vx')
    vy = z3.Real('vy')
    vz = z3.Real('vz')

    solver = z3.Solver()

    for i, stone in enumerate(stones):
        ti = z3.Real(f't{i}')
        solver.add(x + ti * vx == stone.x + ti * stone.vx)
        solver.add(y + ti * vy == stone.y + ti * stone.vy)
        solver.add(z + ti * vz == stone.z + ti * stone.vz)

    solver.check()
    model = solver.model()
    return model.eval(x+y+z)


stones = parse_input(inp)
print('part1:', part1(stones))
print('part2:', part2(stones))
