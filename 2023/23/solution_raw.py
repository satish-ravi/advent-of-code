import sys
from collections import deque
from dataclasses import dataclass
import functools
inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0

rs = len(inp)
cs = len(inp[0])

s = (0, 1)

dir_ops = {
    '.': [(0, 1), (1, 0), (0, -1), (-1, 0)],
    '<': [(0, -1)],
    '>': [(0, 1)],
    '^': [(-1, 0)],
    'v': [(1, 0)],
}

@functools.lru_cache(maxsize=None)
def find_longest_rec(r, c, visited):
    if r == rs - 1:
        return 0
    options = []
    vs = set(visited)
    for (dr, dc) in dir_ops['.']:
        nr, nc = r + dr, c + dc
        if not (0 <= r < rs and 0 <= c < cs):
            continue
        if (nr, nc) in visited or inp[nr][nc] == '#':
            continue
        options.append((nr, nc))
    new_visited = tuple(list(visited) + [(r, c)])
    if not options:
        return 0
    return 1 + max(find_longest_rec(nr, nc, new_visited) for nr, nc in options)

def find_longest(r, c):
    stack = [(r, c, [])]
    max_length = 0

    while stack:
        r, c, visited = stack.pop()
        if r == rs - 1:
            max_length = max(max_length, len(visited))
            continue

        options = []
        vs = set(visited)
        for (dr, dc) in dir_ops[inp[r][c]]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rs and 0 <= nc < cs):
                continue
            if (nr, nc) in visited or inp[nr][nc] == '#':
                continue
            options.append((nr, nc))

        for nr, nc in options:
            new_visited = tuple(list(visited) + [(r, c)])
            stack.append((nr, nc, new_visited))

    return max_length

print(find_longest(0, 1))

def get_neighbors2(r, c):
    n = []
    for dr, dc in dir_ops['.']:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rs and 0 <= nc < cs and inp[nr][nc] != '#':
            n.append((nr, nc))
    return n

hubs = set([(0, 1), (rs - 1, cs - 2)])
for r in range(rs):
    for c in range(cs):
        if inp[r][c] != '#' and len(get_neighbors2(r, c)) > 2:
            hubs.add((r, c))

g = {h: {} for h in hubs}

def hub_neighbors(h, s):
    if s in hubs:
        return {s: 1}
    visited = {h, s}
    end = {}
    q = [(s, 1)]
    while q:
        (r, c), d = q.pop()
        for nr, nc in get_neighbors2(r, c):
            if (nr, nc) in visited:
                continue
            if (nr, nc) in hubs:
                end[(nr, nc)] = d + 1
                continue
            visited.add((nr, nc))
            q.append(((nr, nc), d + 1))
    return end

for h, v in g.items():
    r, c = h
    for s in get_neighbors2(r, c):
        for nh, d in hub_neighbors(h, s).items():
            v[nh] = max(d, v.get(nh, d))

ans = 0
q = [((0, 1), set((0, 1)), 0)]
while q:
    h, visited, d = q.pop()
    for nh, nd in g[h].items():
        if nh in visited:
            continue
        if nh == (rs - 1, cs - 2):
            ans = max(ans, d + nd)
            continue
        q.append((nh, visited | {nh}, d + nd))
print(ans)
