import sys

inp = list(l.strip() for l in sys.stdin.readlines())


def part1(inp):
    cur = 50
    ans = 0

    for line in inp:
        d, n = line[0], int(line[1:])
        if d == 'L':
            cur = (cur - n) % 100
        else:
            cur = (cur + n) % 100
        if cur == 0:
            ans += 1
    return ans


def part2(inp):
    cur = 50
    ans = 0

    for line in inp:
        d, n = line[0], int(line[1:])
        val = 1 if d == 'R' else -1
        for i in range(n):
            cur = (cur + val) % 100
            if cur == 0:
                ans += 1

    return ans

print('part1:', part1(inp))
print('part2:', part2(inp))
