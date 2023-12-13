import sys
import functools

inp = list(l.strip() for l in sys.stdin.readlines())

def solve_row(p, skip=None):
    rs = len(p)
    for r in range(1, rs):
        found = r
        for t in range(r - 1, -1, -1):
            b = r - t + r - 1
            if b >= rs:
                break
            if p[t] != p[b]:
                found = None
                break
        if found and found != skip:
            return r

def solve(p, skip=None):
    r = solve_row(p, skip // 100 if skip else None)
    if r:
        return r * 100
    trs = [''.join(chars) for chars in zip(*p)]
    c = solve_row(trs, skip)
    if c:
        return c
    return None

def solve_smudged(p):
    base = solve(p)
    for r in range(len(p)):
        for c in range(len(p[0])):
            ng = [[x for x in row] for row in p]
            ng[r][c] = '.' if ng[r][c] == '#' else '#'
            new_solve = solve([''.join(row) for row in ng], base)
            if new_solve:
                return new_solve
    print('cannot solve', p, base)

ans = 0
p = []
for r, row in enumerate(inp):
    if row == '':
        ans += solve(p)
        p = []
    else:
        p.append(row)

if p:
    ans+= solve(p)

# print(solve(['##..####..###', '.#..####..#..', '#...#..#...##', '##.#....#.###', '...#.##.#.#..', '.###....###..', '#.########.##', '#..##..##..##', '.#.#....#.#..']))

print(ans)

ans = 0
p = []
for r, row in enumerate(inp):
    if row == '':
        ans += solve_smudged(p)
        p = []
    else:
        p.append(row)

if p:
    ans+= solve_smudged(p)

print(ans)