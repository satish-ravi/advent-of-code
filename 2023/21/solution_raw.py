import sys
from collections import deque
import math
inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0

rs = len(inp)
cs = len(inp[0])

rocks = set([])
s = None

dots = set([])

for r, row in enumerate(inp):
    for c, col in enumerate(row):
        if col == 'S':
            s = (r, c)
            dots.add((r, c))
        elif col == '#':
            rocks.add((r, c))
        else:
            dots.add((r, c))

cur = set([s])
for _ in range(64):
    nex = set()
    for r, c in cur:
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rs and 0 <= nc < cs and (nr, nc) not in rocks:
                nex.add((nr, nc))
    cur = nex

print(len(cur))

cur = set([s])

down_dots = set([])
for r, c in dots:
    down_dots.add((r + rs, c))

steps = 26501365

assert steps % rs == rs // 2

vals = [rs // 2, rs // 2 + rs, rs // 2 + 2 * rs]

required = []

for i in range(vals[-1] + 1):
    nex = set()
    for r, c in cur:
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            nnr = nr % rs
            nnc = nc % cs
            if (nnr, nnc) not in rocks:
                nex.add((nr, nc))
    if i in vals:
        required.append(len(cur))
    cur = nex

v0 = required[0]
v1 = required[1] - required[0]
v2 = required[2] - required[1]

repetitions = steps // rs

print(v0 + v1 * repetitions + (v2 - v1) * (repetitions * (repetitions - 1)) // 2)
