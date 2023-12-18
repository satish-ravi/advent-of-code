import sys
from enum import Enum
import heapq

inp = list(l.strip() for l in sys.stdin.readlines())

DIRECTION_DELTAS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

def parse_input(inp):
    plan = []
    for row in inp:
        d, l_str, col = row.split(' ')
        plan.append((d, int(l_str), col[1:-1]))
    return plan

def solve(plan):
    current = (0, 0)
    coordinates = [current]
    perimeter = 0
    for (direction, length) in plan:
        r, c = current
        dr, dc = DIRECTION_DELTAS[direction]
        nr, nc = r + dr * length, c + dc * length
        coordinates.append((nr, nc))
        current = (nr, nc)
        perimeter += length
    area_twice = 0
    for index in range(len(coordinates) - 1):
        r1, c1 = coordinates[index]
        r2, c2 = coordinates[index + 1]
        area_twice += r1 * c2 - r2 * c1
    return abs(area_twice) // 2 + perimeter // 2 + 1


def part1(plan):
    return solve([(d, l) for d, l, _ in plan])

def part2(plan):
    DIRECTION_INDEX = ['R', 'D', 'L', 'U']
    return solve([(DIRECTION_INDEX[int(color[-1])], int(color[1:-1], 16)) for _, _, color in plan])

plan = parse_input(inp)

print('part1:', part1(plan))
print('part2:', part2(plan))
