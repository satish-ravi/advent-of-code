import sys
from enum import Enum

inp = list(l.strip() for l in sys.stdin.readlines())

class Direction(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class Cell(Enum):
    Empty = '.'
    ForwardMirror = '/'
    BackwardMirror = '\\'
    HorizontalSplitter = '|'
    VerticalSplitter = '-'

def get_enum_member(enum_class, value):
    for member in enum_class:
        if member.value == value:
            return member
    raise ValueError(f"No {enum_class.__name__} member with value {value}")

def get_next_directions(cell, direction):
    if cell == Cell.ForwardMirror:
        return {
            Direction.LEFT: [Direction.DOWN],
            Direction.DOWN: [Direction.LEFT],
            Direction.UP: [Direction.RIGHT],
            Direction.RIGHT: [Direction.UP],
        }[direction]
    if cell == Cell.BackwardMirror:
        return {
            Direction.RIGHT: [Direction.DOWN],
            Direction.DOWN: [Direction.RIGHT],
            Direction.UP: [Direction.LEFT],
            Direction.LEFT: [Direction.UP],
        }[direction]
    if cell == Cell.VerticalSplitter and direction in [Direction.UP, Direction.DOWN]:
        return [Direction.LEFT, Direction.RIGHT]
    if cell == Cell.HorizontalSplitter and direction in [Direction.LEFT, Direction.RIGHT]:
        return [Direction.UP, Direction.DOWN]
    return [direction]

def parse_input(inp):
    grid = []
    for line in inp:
        row = []
        for ch in line:
            row.append(get_enum_member(Cell, ch))
        grid.append(row)
    return grid

def get_next(row, col, direction):
    if direction == Direction.RIGHT:
        return (row, col + 1, direction)
    if direction == Direction.LEFT:
        return (row, col - 1, direction)
    if direction == Direction.UP:
        return (row - 1, col, direction)
    if direction == Direction.DOWN:
        return (row + 1, col, direction)
    raise ValueError(f'Invalid direction {direction}')

def solve(grid, start_row, start_col, start_direction):
    stack = [(start_row, start_col, start_direction)]
    visited = set({})
    rows, cols = len(grid), len(grid[0])
    while stack:
        row, col, direction = stack.pop()
        if not (0 <= row < rows and 0 <= col < cols) or (row, col, direction) in visited:
            continue
        visited.add((row, col, direction))

        for next_dir in get_next_directions(grid[row][col], direction):
            stack.append(get_next(row, col, next_dir))

    return len(set([(row, col) for (row, col, _) in visited]))


def part1(grid):
    return solve(grid, 0, 0, Direction.RIGHT)

def part2(grid):
    result = 0
    rows, cols = len(grid), len(grid[0])
    for start_col in range(cols):
        result = max(result, solve(grid, 0, start_col, Direction.DOWN))
        result = max(result, solve(grid, rows - 1, start_col, Direction.UP))
    for start_row in range(rows):
        result = max(result, solve(grid, start_row, 0, Direction.RIGHT))
        result = max(result, solve(grid, start_row, cols - 1, Direction.LEFT))
    return result

grid = parse_input(inp)

print('part1:', part1(grid))
print('part2:', part2(grid))
