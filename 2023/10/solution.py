import sys
import abc
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass
class Pipe(abc.ABC):
    row: int
    col: int

    @classmethod
    @abc.abstractmethod
    def valid_dir(self):
        pass

    @classmethod
    @abc.abstractmethod
    def next_dir(self, dir):
        pass

    @classmethod
    @abc.abstractmethod
    def next_delta(self, dir):
        pass

    def next_node(self, dir):
        assert dir in self.valid_dir(), f'${dir}, ${self}'
        dr, dc = self.next_delta(dir)
        return (self.row + dr, self.col + dc)

    def apply_deltas(self, deltas):
        return [(self.row + r, self.col + c) for r, c in deltas]

    @classmethod
    @abc.abstractmethod
    def get_side_deltas(self, dir):
        pass

    def get_sides(self, dir):
        assert dir in self.valid_dir(), f'${dir}, ${self}'
        # clockwise
        outer, inner = self.get_side_deltas(dir)
        return (self.apply_deltas(outer), self.apply_deltas(inner))

@dataclass
class Horizontal(Pipe):
    @classmethod
    def valid_dir(cls):
        return ['E', 'W']

    @classmethod
    def next_dir(cls, dir):
        return dir

    @classmethod
    def next_delta(cls, dir):
        return (0, -1) if dir == 'W' else (0, 1)

    @classmethod
    def get_side_deltas(cls, dir):
        side1 = [(1, 0)]
        side2 = [(-1, 0)]

        return (side1, side2) if dir == 'W' else (side2, side1)

@dataclass
class Vertical(Pipe):
    @classmethod
    def valid_dir(self):
        return ['N', 'S']

    @classmethod
    def next_dir(cls, dir):
        return dir

    @classmethod
    def next_delta(cls, dir):
        return (-1, 0) if dir == 'N' else (1, 0)

    @classmethod
    def get_side_deltas(cls, dir):
        side1 = [(0, 1)]
        side2 = [(0, -1)]

        return (side1, side2) if dir == 'S' else (side2, side1)

@dataclass
class NW(Pipe):
    @classmethod
    def valid_dir(cls):
        return ['N', 'W']

    @classmethod
    def next_dir(cls, dir):
        return 'E' if dir == 'N' else 'S'

    @classmethod
    def next_delta(cls, dir):
        return (0, 1) if dir == 'N' else (1, 0)

    @classmethod
    def get_side_deltas(cls, dir):
        side = [(0, -1), (-1, -1), (-1, 0)]

        return (side, []) if dir == 'N' else ([], side)

@dataclass
class NE(Pipe):
    @classmethod
    def valid_dir(cls):
        return ['N', 'E']

    @classmethod
    def next_dir(cls, dir):
        return 'W' if dir == 'N' else 'S'

    @classmethod
    def next_delta(cls, dir):
        return (0, -1) if dir == 'N' else (1, 0)

    @classmethod
    def get_side_deltas(cls, dir):
        side = [(-1, 0), (-1, 1), (0, 1)]

        return (side, []) if dir == 'E' else ([], side)

@dataclass
class SE(Pipe):
    @classmethod
    def valid_dir(cls):
        return ['S', 'E']

    @classmethod
    def next_dir(cls, dir):
        return 'W' if dir == 'S' else 'N'

    @classmethod
    def next_delta(cls, dir):
        return (0, -1) if dir == 'S' else (-1, 0)

    @classmethod
    def get_side_deltas(cls, dir):
        side = [(0, 1), (1, 1), (1, 0)]

        return (side, []) if dir == 'S' else ([], side)

@dataclass
class SW(Pipe):
    @classmethod
    def valid_dir(cls):
        return ['S', 'W']

    @classmethod
    def next_dir(self, dir):
        return 'E' if dir == 'S' else 'N'

    @classmethod
    def next_delta(cls, dir):
        return (0, 1) if dir == 'S' else (-1, 0)

    @classmethod
    def get_side_deltas(cls, dir):
        side = [(1, 0), (1, -1), (0, -1)]

        return (side, []) if dir == 'W' else ([], side)

def get_start_pipe(inp):
    rows = len(inp)
    cols = len(inp[0])
    start = None
    for r in range(rows):
        for c in range(cols):
            if inp[r][c] == 'S':
                start = (r, c)
                break
        if start:
            break

    r, c = start
    connected_east = c != cols - 1 and inp[r][c+1] in ['J', '7', '-']
    connected_west = c != 0 and inp[r][c-1] in ['F', '-', 'L']
    connected_north = r != 0 and inp[r-1][c] in ['F', '|', '7']
    connected_south = r != rows - 1 and inp[r+1][c] in ['J', '|', 'L']

    if connected_north and connected_west:
        return 'J'
    if connected_north and connected_east:
        return 'L'
    if connected_south and connected_west:
        return '7'
    if connected_south and connected_east:
        return 'F'
    if connected_north and connected_south:
        return '|'
    if connected_east and connected_west:
        return '-'
    raise Exception('Cannot determine start pipe')

def parse_input(inp):
    grid = []
    rows = len(inp) + 2
    cols = len(inp[0]) + 2
    start = None
    for r in range(rows):
        row = []
        for c in range(cols):
            if r == 0 or c == 0 or r == rows - 1 or c == cols - 1:
                row.append(None)
                continue
            val = inp[r-1][c-1]
            if val == '.':
                row.append(None)
                continue
            if val == 'S':
                start = (r, c)
                val = get_start_pipe(inp)
            if val == 'F':
                row.append(NW(r, c))
            elif val == '7':
                row.append(NE(r, c))
            elif val == 'J':
                row.append(SE(r, c))
            elif val == 'L':
                row.append(SW(r, c))
            elif val == '-':
                row.append(Horizontal(r, c))
            elif val == '|':
                row.append(Vertical(r, c))
            else:
                raise Exception(f'Invalid value : {val}, at {(r, c)}')
        grid.append(row)
    return start, grid


def traverse_loop(grid, start):
    outers, inners = [], []
    loop_pipes = []
    current = start
    dir = grid[start[0]][start[1]].valid_dir()[0]

    while not loop_pipes or current != start:
        r, c = current
        loop_pipes.append((r, c))
        pipe = grid[r][c]
        # print(current, pipe, dir)
        outs, ins = pipe.get_sides(dir)
        outers.extend(outs)
        inners.extend(ins)
        current = pipe.next_node(dir)
        dir = pipe.next_dir(dir)

    return loop_pipes, outers, inners


def part1(start, grid):
    loop_pipes, outers, inner = traverse_loop(grid, start)
    return len(loop_pipes) // 2

def part2(start, grid):
    loop_pipes, outers, inners = traverse_loop(grid, start)

    def fill_grid(nodes, val):
        stack = set(nodes)
        while stack:
            r, c = stack.pop()
            if not(0 <= r < len(grid) and 0 <= c < len(grid[0])) or (r, c) in loop_pipes or grid[r][c] in ['I', 'O']:
                continue
            grid[r][c] = val
            stack.add((r + 1, c))
            stack.add((r - 1, c))
            stack.add((r, c + 1))
            stack.add((r, c - 1))

    fill_grid(outers, 'O')
    fill_grid(inners, 'I')
    res_char = 'I' if grid[0][0] == 'O' else 'O'
    result = 0
    for row in grid:
        for val in row:
            if val == res_char:
                result += 1
    return result



start, grid = parse_input(inp)
print('part1:', part1(start, grid))
print('part2:', part2(start, grid))
