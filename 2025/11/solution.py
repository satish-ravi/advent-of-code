import sys
from collections import defaultdict
from functools import cache

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    connections = defaultdict(list)
    for line in inp:
        left, right = line.split(': ')
        connections[left] = right.split(' ')
    return connections

def part1(connections):
    @cache
    def count_paths(node):
        if node == 'out':
            return 1

        return sum(count_paths(next) for next in connections[node])

    return count_paths('you')

def part2(connections):
    @cache
    def count_paths(node, visited_fft, visited_dac):
        if node == 'out':
            return int(visited_fft and visited_dac)

        if node == 'fft':
            visited_fft = True
        if node == 'dac':
            visited_dac = True
        return sum(count_paths(next_node, visited_fft, visited_dac) for next_node in connections[node])

    return count_paths('svr', False, False)

connections = parse_input(inp)
print('part1:', part1(connections))
print('part2:', part2(connections))
