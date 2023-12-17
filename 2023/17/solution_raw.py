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

op = {
    'R': 'L', 'L': 'R', 'D': 'U', 'U': 'D'
}

init = (0, 0, 'R', 0)
dis = {init: 0}

pq = [(0, init)]
seen = set()
while pq:
    cdi, cur = heapq.heappop(pq)

    (r, c, d, dl) = cur

    if cur in seen:
        continue
    seen.add(cur)

    for nd, (dr, dc) in dirs.items():
        nr = r + dr
        nc = c + dc
        if not (0 <= nr < rs and 0 <= nc < cs):
            continue
        if d == nd and dl == 3 or nd == op[d]:
            continue
        ndi = cdi + int(inp[nr][nc])
        nx = (nr, nc, nd, 1 + (dl if d == nd else 0))

        if nx in dis and dis[nx] < ndi:
            continue
        dis[nx] = ndi
        heapq.heappush(pq, (ndi, nx))

print(min(v for k,v in dis.items() if k[0] == rs - 1 and k[1] == cs - 1))

init = (0, 0, 'R', 0)
dis = {init: 0}

pq = [(0, init)]
seen = set()
while pq:
    cdi, cur = heapq.heappop(pq)

    (r, c, d, dl) = cur

    if cur in seen:
        continue
    seen.add(cur)

    for nd, (dr, dc) in dirs.items():
        nr = r + dr
        nc = c + dc
        if not (0 <= nr < rs and 0 <= nc < cs):
            continue
        if (dl != 0 and d != nd and dl < 4) or (d == nd and dl == 10) or nd == op[d]:
            continue
        ndi = cdi + int(inp[nr][nc])
        nx = (nr, nc, nd, 1 + (dl if d == nd else 0))

        if nx in dis and dis[nx] < ndi:
            continue
        dis[nx] = ndi
        heapq.heappush(pq, (ndi, nx))

print(min(v for k,v in dis.items() if k[0] == rs - 1 and k[1] == cs - 1 and k[3] >= 4))
