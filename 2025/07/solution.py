from collections import deque
import sys
from functools import cache

inp = list(l for l in sys.stdin.readlines())


def parse_input(inp):
    R, C = len(inp), len(inp[0])
    start = None
    for r in range(R):
        for c in range(C):
            if inp[r][c] == 'S':
                start = (r, c)
                break
        if start is not None:
            break
    return inp, start, R


def part1(grid, start, R):
    q = deque([(start[0] + 1, start[1])])
    visited = set([(start[0] + 1, start[1])])
    splits = 0
    while q:
        r, c = q.popleft()
        nr, nc = r + 1, c
        if nr == R:
            continue
        if grid[nr][nc] == '^':
            splits += 1
            if (nr, nc - 1) not in visited:
                q.append((nr, nc - 1))
                visited.add((nr, nc - 1))
            if (nr, nc + 1) not in visited:
                q.append((nr, nc + 1))
                visited.add((nr, nc + 1))
        else:
            if (nr, nc) not in visited:
                q.append((nr, nc))
                visited.add((nr, nc))
    return splits

def part2(grid, start, R):
    @cache
    def get_timelines(r, c):
        if r == R - 1:
            return 1
        nr, nc = r + 1, c
        if grid[nr][nc] == '^':
            return get_timelines(nr, nc - 1) + get_timelines(nr, nc + 1)
        else:
            return get_timelines(nr, nc)

    return get_timelines(start[0] + 1, start[1])

grid, start, R = parse_input(inp)
print('part1:', part1(grid, start, R))
print('part2:', part2(grid, start, R))
