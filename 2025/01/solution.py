import sys

inp = list(l.strip() for l in sys.stdin.readlines())


def parse_input(inp):
    return [(line[0], int(line[1:])) for line in inp]


DIRS = {
    'L': -1,
    'R': 1,
}


def part1(instructions):
    cur = 50
    ans = 0

    for direction, n in instructions:
        cur = (cur + n * DIRS[direction]) % 100
        if cur == 0:
            ans += 1
    return ans


def part2(instructions):
    cur = 50
    ans = 0

    for direction, n in instructions:
        next_before_rounding = cur + n * DIRS[direction]
        ans += abs(next_before_rounding // 100)
        if direction == 'L' and cur == 0:
            ans -= 1
        cur = next_before_rounding % 100
        if direction == 'L' and cur == 0:
            ans += 1

    return ans

instructions = parse_input(inp)
print('part1:', part1(instructions))
print('part2:', part2(instructions))
