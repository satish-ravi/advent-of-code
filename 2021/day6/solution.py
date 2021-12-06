from collections import defaultdict
import sys

def read_input() -> list[int]:
    inp = list(l.strip() for l in sys.stdin.readlines())
    return [int(n) for n in inp[0].split(",")]

def compute(initial: list[int], days: int) -> int:
    fishes = defaultdict(int)
    for f in initial:
        fishes[f] += 1

    for _ in range(days):
        new_fishes = defaultdict(int)
        for fish, count in fishes.items():
            if fish == 0:
                new_fishes[6] += count
                new_fishes[8] = count
            else:
                new_fishes[fish - 1] += count
        fishes = new_fishes

    return sum(fishes.values())

inp = read_input()
print("part1:", compute(inp, 80))
print("part2:", compute(inp, 256))
