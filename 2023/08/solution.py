import sys
from dataclasses import dataclass

import sys
import re
import math

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    mapping = {}

    for row in inp[2:]:
        k, v = row.split(' = ')
        l, r = v[1:-1].split(', ')
        mapping[k] = {'L': l, 'R': r}

    return inp[0], mapping

def create_next_move_generator(moves):
    i = 0
    while True:
        yield moves[i]
        i = (i + 1) % len(moves)


def solve(start, end_rule, moves, mapping):
    moves_gen = create_next_move_generator(moves)
    result = 0
    val = start
    while not end_rule(val):
        val = mapping[val][next(moves_gen)]
        result += 1
    return result

def lcm_of_list(numbers):
    if len(numbers) == 0:
        raise ValueError("List must contain at least one number.")

    result = numbers[0]

    for num in numbers[1:]:
        result = abs(result * num) // math.gcd(result, num)

    return result


def part1(moves, mapping):
    return solve('AAA', lambda val: val == 'ZZZ', moves, mapping)

def part2(moves, mapping):
    end_rule = lambda val: val[-1] == 'Z'
    return lcm_of_list([solve(k, end_rule, moves, mapping) for k in mapping.keys() if k[-1] == 'A'])


moves, mapping = parse_input(inp)
print('part1:', part1(moves, mapping))
print('part2:', part2(moves, mapping))