import sys
import math

inp = list(l.strip() for l in sys.stdin.readlines())

def num_winning(time, distance):
    win_start = next((hold for hold in range(1, time) if hold * (time - hold) > distance), None)
    win_end = next((hold for hold in range(time - 1, 0, -1) if hold * (time - hold) > distance), None)
    return win_end - win_start + 1 if win_end is not None and win_start is not None else 0


def part1(inp):
    ts = [int(n) for n in inp[0].split(': ')[1].strip().split(' ') if n]
    ds = [int(n) for n in inp[1].split(': ')[1].strip().split(' ') if n]
    return math.prod(num_winning(time, distance) for time, distance in zip(ts, ds))

def part2(inp):
    time = int(inp[0].split(': ')[1].replace(' ', ''))
    distance = int(inp[1].split(': ')[1].replace(' ', ''))
    return num_winning(time, distance)

print('part1:', part1(inp))
print('part2:', part2(inp))
