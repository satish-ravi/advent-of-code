import sys
from collections import Counter

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    return [list(map(int, l.split('-'))) for l in inp[0].split(',')]


def solve(ranges, is_invalid_fn):
    total = 0
    for l, r in ranges:
        for n in range(l, r + 1):
            if is_invalid_fn(n):
                total += n
    return total


def part1(ranges):
    def is_invalid_fn(n):
        n_str = str(n)
        return n_str[:len(n_str)//2] == n_str[len(n_str)//2:]

    return solve(ranges, is_invalid_fn)

def part2(ranges):
    def is_invalid_fn(n):
        n_str = str(n)
        L = len(n_str)
        for d in range(1, len(n_str) // 2 + 1):
            if len(n_str) % d != 0:
                continue
            if n_str[0:d] * (L // d) == n_str:
                return True
    return solve(ranges, is_invalid_fn)

ranges = parse_input(inp)
print('part1:', part1(ranges))
print('part2:', part2(ranges))
