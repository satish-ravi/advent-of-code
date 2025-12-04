import sys

inp = list(l.strip() for l in sys.stdin.readlines())

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def part1(inp):
    ans = 0
    R, C = len(inp), len(inp[0])
    for r in range(R):
        for c in range(C):
            if inp[r][c] == '.':
                continue
            adjacent = 0
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                if inp[nr][nc] == '@':
                    adjacent += 1
            if adjacent < 4:
                ans += 1
    return ans

def part2(inp):
    R, C = len(inp), len(inp[0])
    rolls = set()
    ans = 0
    for r in range(R):
        for c in range(C):
            if inp[r][c] == '.':
                continue
            rolls.add((r, c))

    while True:
        to_remove = set()
        for r, c in rolls:
            adjacent = 0
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                if (nr, nc) in rolls:
                    adjacent += 1
            if adjacent < 4:
                to_remove.add((r, c))

        if not to_remove:
            break
        ans += len(to_remove)
        rolls -= to_remove
    return ans

print('part1:', part1(inp))
print('part2:', part2(inp))
