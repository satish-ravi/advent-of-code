import sys
import functools

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    grid = []
    for row in inp:
        grid.append([c for c in row])
    return grid

def transpose(grid):
    return list(map(list, zip(*grid)))

def slide(grid, dir):
    base_grid = grid if dir in ['east', 'west'] else transpose(grid)

    rows = len(base_grid)
    cols = len(base_grid[0])

    slid_grid = []
    for r in range(rows):
        new_row = []
        spaces = rounded = 0
        col_range = range(cols) if dir in ['north', 'west'] else range(cols-1, -1, -1)
        for c in col_range:
            if base_grid[r][c] == '.':
                spaces += 1
            elif base_grid[r][c] == 'O':
                rounded += 1
            else:
                new_row.extend(['O'] * rounded)
                new_row.extend(['.'] * spaces)
                new_row.append('#')
                spaces = rounded = 0
        new_row.extend(['O'] * rounded)
        new_row.extend(['.'] * spaces)
        slid_grid.append(new_row if dir in ['north', 'west'] else new_row[::-1])
    return slid_grid if dir in ['east', 'west'] else transpose(slid_grid)

def spin(grid):
    for dir in ['north', 'west', 'south', 'east']:
        grid = slide(grid, dir)
    return grid

def total_load(grid):
    result = 0
    for r, row in enumerate(grid):
        result += sum([len(grid) - r for c in row if c == 'O'])
    return result

def is_equal(g1, g2):
    for r in range(len(g1)):
        for c in range(len(g2)):
            if g1[r][c] != g2[r][c]:
                return False
    return True

def part1(grid):
    return total_load(slide(grid, 'north'))

def part2(grid):
    current_grid = grid
    cycled_grids = [current_grid]
    repeat_index = None

    while not repeat_index:
        next_grid = spin(current_grid)
        for spin_count, grid in enumerate(cycled_grids):
            if is_equal(grid, next_grid):
                repeat_index = spin_count
                break
        cycled_grids.append(next_grid)
        current_grid = next_grid

    final_grid_index = (1000000000 - repeat_index) % (len(cycled_grids) - 1 - repeat_index) + repeat_index

    return total_load(cycled_grids[final_grid_index])

grid = parse_input(inp)

print('part1:', part1(grid))
print('part2:', part2(grid))
