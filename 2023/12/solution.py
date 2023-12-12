import sys
import functools

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    parsed = []
    for row in inp:
        springs, damaged_groups_str = row.split(' ')
        damaged_groups = tuple([int(group) for group in damaged_groups_str.split(',')])
        parsed.append((springs, damaged_groups))
    return parsed

@functools.lru_cache(maxsize=None)
def solve(springs, damaged_groups, current_group_len):
    if springs == '':
        if len(damaged_groups) == 0 and not current_group_len or len(damaged_groups) == 1 and damaged_groups[0] == current_group_len:
            return 1
        return 0
    remaining_damaged = len([spring for spring in springs if spring == '#'])
    remaining_unknown = len([spring for spring in springs if spring == '?'])

    if remaining_damaged + remaining_unknown + (current_group_len or 0) < sum(damaged_groups) or remaining_damaged > sum(damaged_groups):
        return 0
    if current_group_len:
        if current_group_len == damaged_groups[0]:
            return solve(springs[1:], damaged_groups[1:], None) if springs[0] in ['?', '.'] else 0
        else:
            return solve(springs[1:], damaged_groups, current_group_len + 1) if springs[0] in ['?', '#'] else 0
    else:
        result = 0
        if springs[0] in ['.', '?']:
            result += solve(springs[1:], damaged_groups, None)
        if springs[0] in ['#', '?'] and damaged_groups:
            result += solve(springs[1:], damaged_groups, 1)
        return result

def part1(parsed):
    return sum([solve(springs, damaged_groups, None) for springs, damaged_groups in parsed])

def part2(parsed):
    return sum([solve(((springs + '?') * 5)[:-1], damaged_groups * 5, None) for springs, damaged_groups in parsed])

parsed = parse_input(inp)
print('part1:', part1(parsed))
print('part2:', part2(parsed))
