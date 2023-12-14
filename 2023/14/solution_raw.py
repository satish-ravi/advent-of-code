import sys
import functools

inp = list(l.strip() for l in sys.stdin.readlines())

new_grid = []
for c in range(len(inp[0])):
    new_c = []
    td = 0
    to = 0
    for r in range(len(inp)):
        if  inp[r][c] == '.':
            td += 1
        elif inp[r][c] == 'O':
            to += 1
        else:
            new_c.extend(['O'] * to)
            new_c.extend(['.'] * td)
            new_c.append('#')
            td = to = 0
    new_c.extend(['O'] * to)
    new_c.extend(['.'] * td)
    new_grid.append(new_c)
ans = 0
for col in new_grid:
    for r, row in enumerate(col):
        if row == 'O':
            ans += len(inp) - r

print(ans)


def is_equal(g1, g2):
    for r in range(len(g1)):
        for c in range(len(g2)):
            if g1[r][c] != g2[r][c]:
                return False

    return True

def transpose(grid):
    return [''.join(chars) for chars in zip(*grid)]

def spin(grid):
    # north
    new_grid = []
    for c in range(len(grid[0])):
        new_c = []
        td = 0
        to = 0
        for r in range(len(grid)):
            if grid[r][c] == '.':
                td += 1
            elif grid[r][c] == 'O':
                to += 1
            else:
                new_c.extend(['O'] * to)
                new_c.extend(['.'] * td)
                new_c.append('#')
                td = to = 0
        new_c.extend(['O'] * to)
        new_c.extend(['.'] * td)
        new_grid.append(new_c)
    grid = transpose(new_grid)
    # west
    new_grid = []
    for r in range(len(grid)):
        new_r = []
        td = 0
        to = 0
        for c in range(len(grid[0])):
            if grid[r][c] == '.':
                td += 1
            elif grid[r][c] == 'O':
                to += 1
            else:
                new_r.extend(['O'] * to)
                new_r.extend(['.'] * td)
                new_r.append('#')
                td = to = 0
        new_r.extend(['O'] * to)
        new_r.extend(['.'] * td)
        new_grid.append(new_r)
    grid = new_grid
    # south
    new_grid = []
    for c in range(len(grid[0])):
        new_c = []
        td = 0
        to = 0
        for r in range(len(grid) - 1, -1, -1):
            if grid[r][c] == '.':
                td += 1
            elif grid[r][c] == 'O':
                to += 1
            else:
                new_c.extend(['O'] * to)
                new_c.extend(['.'] * td)
                new_c.append('#')
                td = to = 0
        new_c.extend(['O'] * to)
        new_c.extend(['.'] * td)
        new_grid.append(new_c[::-1])
    grid = transpose(new_grid)
    # east
    new_grid = []
    for r in range(len(grid)):
        new_r = []
        td = 0
        to = 0
        for c in range(len(grid[0]) -1, -1, -1):
            if grid[r][c] == '.':
                td += 1
            elif grid[r][c] == 'O':
                to += 1
            else:
                new_r.extend(['O'] * to)
                new_r.extend(['.'] * td)
                new_r.append('#')
                td = to = 0
        new_r.extend(['O'] * to)
        new_r.extend(['.'] * td)
        new_grid.append(new_r[::-1])
    return new_grid

cur = inp
cache = [cur]
spins = 0
repeat = None

while not repeat:
    nxt = spin(cur)
    spins += 1
    for sp, grid in enumerate(cache):
        if is_equal(grid, nxt):
            repeat = sp
            break
    cache.append(nxt)
    cur = nxt

final = (1000000000 - repeat) % (spins - repeat) + repeat

ans = 0
for r, row in enumerate(cache[final]):
    for c in row:
        if c == 'O':
            ans += len(inp) - r

print(ans)
