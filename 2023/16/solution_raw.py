import sys
from collections import deque
inp = list(l.strip() for l in sys.stdin.readlines())

ds = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

def solve(sr, sc, sdir):

    q = deque([(sr, sc, sdir)])
    visited = set({})
    while q:
        r, c, dir = q.popleft()
        if not (0 <= r < len(inp) and 0 <= c < len(inp[0])) or (r, c, dir) in visited:
            continue
        visited.add((r, c, dir))
        if inp[r][c] == '|' and dir in ['L', 'R']:
            q.append((r + 1, c, 'D'))
            q.append((r - 1, c, 'U'))
        elif inp[r][c] == '-' and dir in ['U', 'D']:
            q.append((r, c+1, 'R'))
            q.append((r, c-1, 'L'))
        else:
            new_dir = dir
            if inp[r][c] == '/':
                new_dir = {'U': 'R', 'D': 'L', 'R': 'U', 'L': 'D'}[dir]
            elif inp[r][c] == '\\':
                new_dir = {'U': 'L', 'D': 'R', 'R': 'D', 'L': 'U'}[dir]
            q.append((r + ds[new_dir][0], c + ds[new_dir][1], new_dir))


    vc = set([(r, c) for (r, c, dir) in visited])
    return len(vc)

print(solve(0,0,'R'))

ans = 0
for sc in range(len(inp[0])):
    ans = max(ans, solve(0, sc, 'D'))
    ans = max(ans, solve(len(inp)-1, sc, 'U'))

for sr in range(len(inp)):
    ans = max(ans, solve(sr, 0, 'R'))
    ans = max(ans, solve(sr, len(inp[0])-1, 'L'))

print(ans)
