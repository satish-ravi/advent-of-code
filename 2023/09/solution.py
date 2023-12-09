import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    return [[int(n) for n in line.split()] for line in inp]


def get_next_sequence(seq, is_forward=True):
    if all(x == 0 for x in seq):
        return 0
    diff_seq = []
    for i in range(len(seq) - 1):
        diff_seq.append(seq[i + 1] - seq[i])
    next_element = get_next_sequence(diff_seq, is_forward)
    return seq[-1] + next_element if is_forward else seq[0] - next_element

def solve(sequences, is_forward):
    return sum([get_next_sequence(seq, is_forward) for seq in sequences])

sequences = parse_input(inp)

print('part1:', solve(sequences, True))
print('part2:', solve(sequences, False))
