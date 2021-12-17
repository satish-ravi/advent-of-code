import re
import sys
from typing import Optional


def read_input() -> tuple[tuple[int, int], tuple[int, int]]:
    inp = sys.stdin.read().split("\n")[0]
    search = re.search("^target area: x=(.*), y=(.*)$", inp)

    x1, x2 = search.group(1).split("..")
    y1, y2 = search.group(2).split("..")

    return ((int(x1), int(x2)), ((int(y1), int(y2))))


def simulate(
    vel_x: int, vel_y: int, x1: int, x2: int, y1: int, y2: int
) -> Optional[int]:
    x, y = 0, 0
    max_y = 0

    while True:
        x += vel_x
        y += vel_y

        if vel_x > 0:
            vel_x -= 1
        elif vel_x < 0:
            vel_x += 1
        vel_y -= 1

        if y > max_y:
            max_y = y

        if x1 <= x <= x2 and y1 <= y <= y2:
            return max_y

        if x > x2 or y < y1:
            return None


def solve(x1: int, x2: int, y1: int, y2: int) -> tuple[int, int]:
    max_y = 0
    count = 0
    for x in range(1, x2 + 1):
        for y in range(y1, -y1 + 1):
            cur = simulate(x, y, x1, x2, y1, y2)
            if cur is not None:
                count += 1
                if cur > max_y:
                    max_y = cur

    return (max_y, count)


(x1, x2), (y1, y2) = read_input()
p1, p2 = solve(x1, x2, y1, y2)
print("part1:", p1)
print("part2:", p2)
