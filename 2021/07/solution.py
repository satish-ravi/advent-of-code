import sys
from typing import Callable


def read_input() -> list[int]:
    inp = list(l.strip() for l in sys.stdin.readlines())
    return [int(x) for x in inp[0].split(",")]


def compute(positions: list[int], cost_fn: Callable[[int], int]) -> int:
    cur_min = 1000000000000
    for i in range(min(positions), max(positions)):
        cur = 0
        for p in positions:
            cur += cost_fn(abs(p - i))
        if cur < cur_min:
            cur_min = cur
    return cur_min


inp = read_input()
print("part1:", compute(inp, lambda n: n))
print("part2:", compute(inp, lambda n: n * (n + 1) // 2))
