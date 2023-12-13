import sys
import functools

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    grids = []
    grid = []
    for row in inp:
        if row == '':
            grids.append(grid)
            grid = []
        else:
            grid.append(row)
    if grid:
        grids.append(grid)
    return grids

def transpose(grid):
    return [''.join(chars) for chars in zip(*grid)]

def count_different_characters(str1, str2):
    # Ensure both strings have the same length
    if len(str1) != len(str2):
        raise ValueError("Both strings must have the same length.")

    # Count the number of different characters
    count = sum(ch1 != ch2 for ch1, ch2 in zip(str1, str2))

    return count

def find_horizontal_mirror(grid, max_delta=0):
    rows = len(grid)
    for r in range(1, rows):
        # mirror is above row r
        delta = 0
        for top in range(r - 1, -1, -1):
            bottom = 2 * r - top - 1
            if bottom >= rows:
                break
            delta += count_different_characters(grid[top], grid[bottom])
            if delta > max_delta:
                break
        if delta == max_delta:
            return r

def solve_grid(grid, max_delta=0):
    row = find_horizontal_mirror(grid, max_delta)
    if row:
        return row * 100
    col = find_horizontal_mirror(transpose(grid), max_delta)
    if col:
        return col
    raise Exception(f'Cannot solve: {grid}')

def solve(grids, max_delta=0):
    return sum([solve_grid(grid, max_delta) for grid in grids])

grids = parse_input(inp)
print('part1:', solve(grids, 0))
print('part2:', solve(grids, 1))
