import sys

inp = list(l.strip() for l in sys.stdin.readlines())

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def parse_input(inp):
    rolls = set()
    for r in range(len(inp)):
        for c in range(len(inp[r])):
            if inp[r][c] == '@':
                rolls.add((r, c))
    return rolls

def get_adjacent(r, c, rolls):
    adjacent = 0
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if (nr, nc) in rolls:
            adjacent += 1
    return adjacent

def part1(rolls):
    ans = 0
    for r, c in rolls:
        if get_adjacent(r, c, rolls) < 4:
            ans += 1
    return ans

def part2(rolls):
    ans = 0
    local_rolls = set(rolls)

    while True:
        to_remove = set()
        for r, c in local_rolls:
            if get_adjacent(r, c, local_rolls) < 4:
                to_remove.add((r, c))

        if not to_remove:
            break
        ans += len(to_remove)
        local_rolls -= to_remove
    return ans

rolls = parse_input(inp)
print('part1:', part1(rolls))
print('part2:', part2(rolls))
