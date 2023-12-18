import sys
from collections import deque
import heapq
inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0
rs = len(inp)
cs = len(inp[0])

dirs = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

sides = {
    'R': [dirs['U'], dirs['D']],
    'L': [dirs['D'], dirs['U']],
    'U': [dirs['L'], dirs['R']],
    'D': [dirs['R'], dirs['L']]
}

op = {
    'R': 'L', 'L': 'R', 'D': 'U', 'U': 'D'
}

def solve(ins):
    ans = 0
    cur = (0, 0)
    dug = set([cur])
    s1 = set([])
    s2 = set([])

    for d, l in ins:
        side1, side2 = sides[d]
        for _ in range(int(l)):
            cr, cc = cur
            nr, nc = cr + dirs[d][0], cc + dirs[d][1]
            dug.add((nr, nc))
            s1.add((nr + side1[0], nc + side1[1]))
            s2.add((nr + side2[0], nc + side2[1]))
            cur = (nr, nc)

    rs = [d[0] for d in dug]
    cs = [d[1] for d in dug]

    minr = min(rs)
    minc = min(cs)
    maxr = max(rs)
    maxc = max(cs)

    s1 = s1 - dug
    s2 = s2 - dug

    # for r in range(minr-1, maxr + 2):
    #     for c in range(minc-1, maxc + 2):
    #         ch = '.'
    #         if (r, c) in dug:
    #             ch = '#'
    #         elif (r, c) in s1:
    #             ch = '1'
    #         elif (r, c) in s2:
    #             ch = '2'
    #         print(ch, end='')
    #     print()

    # print(minr, minc, maxr, maxc)

    grid = [['.' for _ in range(minc - 1, maxc + 2)] for _ in range(minr - 1, maxr + 2)]

    def fill_grid(nodes, val):
        stack = set(nodes)
        while stack:
            r, c = stack.pop()
            ar, ac = r - (minr - 1), c - (minc - 1)
            # print(r, c, ar, ac)
            # break
            if not(0 <= ar < len(grid) and 0 <= ac < len(grid[0])) or (r, c) in dug or grid[ar][ac] in ['1', '2']:
                continue
            grid[ar][ac] = val
            stack.add((r + 1, c))
            stack.add((r - 1, c))
            stack.add((r, c + 1))
            stack.add((r, c - 1))

    fill_grid(s1, '1')
    fill_grid(s2, '2')

    for row in grid:
        for col in row:
            if col != grid[0][0]:
                ans += 1

# for row in grid:
#     print(''.join(row))

    return ans



def solve2(ins):
    cur = (0, 0)
    coords = [cur]
    tl = 0
    for d, l in ins:
        cr, cc = cur
        dr, dc = dirs[d]
        nr, nc = cr + dr * l, cc + dc * l
        coords.append((nr, nc))
        cur = (nr, nc)
        tl += l
    res = 0
    for i in range(len(coords) - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i+1]
        res += x1 * y2 - x2 * y1
    return abs(res) // 2 + tl // 2 + 1

ins = []

for row in inp:
    d, l, _ = row.split(' ')
    ins.append((d, int(l)))

print(solve(ins))
print(solve2(ins))

ins = []
for row in inp:
    d = ['R', 'D', 'L', 'U'][int(row[-2])]
    l = int(row[-7:-2], 16)
    ins.append((d, l))

print(solve2(ins))
