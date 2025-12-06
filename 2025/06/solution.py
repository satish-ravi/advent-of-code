from math import prod
import sys

inp = list(l for l in sys.stdin.readlines())


def part1(inp):
    lines = []
    for row in inp[:-1]:
        lines.append(list(map(int, row.split())))

    ops = inp[-1].split()

    ans = 0
    for i, op in enumerate(ops):
        res = 0 if op == '+' else 1
        for line in lines:
            if op == '+':
                res += line[i]
            elif op == '*':
                res *= line[i]
        ans += res
    return ans

def part2(inp):
    R, C = len(inp), len(inp[0])
    ans = 0
    nums = []
    for c in range(C-1, -1, -1):
        col = ''.join(inp[r][c] for r in range(R-1)).strip()
        if col == '':
            continue
        nums.append(int(col))
        if inp[-1][c] == '+':
            ans += sum(nums)
            nums = []
        elif inp[-1][c] == '*':
            ans += prod(nums)
            nums = []

    return ans


print('part1:', part1(inp))
print('part2:', part2(inp))
