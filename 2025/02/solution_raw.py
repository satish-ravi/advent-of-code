import sys
from collections import Counter

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    return [list(map(int, l.split('-'))) for l in inp[0].split(',')]


def part1(ranges):
    total = 0
    for l, r in ranges:
        for n in range(l, r + 1):
            n_str = str(n)
            if n_str[:len(n_str)//2] == n_str[len(n_str)//2:]:
                total += n
    return total


def part2(ranges):
    total = 0
    for l, r in ranges:
        for n in range(l, r + 1):
            n_str = str(n)
            for d in range(1, len(n_str) // 2 + 1):
                if len(n_str) % d != 0:
                    continue
                if all(n_str[0:d] == n_str[i:i+d] for i in range(d, len(n_str), d)):
                    total += n
                    break
    return total

ranges = parse_input(inp)
print('part1:', part1(ranges))
print('part2:', part2(ranges))
