import sys
from enum import Enum
import heapq

inp = list(l.strip() for l in sys.stdin.readlines())

DIRECTION_DELTAS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

OPPOSITES = {
    'R': 'L', 'L': 'R', 'D': 'U', 'U': 'D'
}

def parse_input(inp):
    return [[int(digit) for digit in line] for line in inp]

def solve(grid, min_dist, max_dist):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0, 'R', 0)
    distances = {start: 0}

    priority_queue = [(0, start)]
    visited = set()

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        visited.add(current)
        (r, c, direction, dir_dist) = current

        for next_dir, (dr, dc) in DIRECTION_DELTAS.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if next_dir == OPPOSITES[direction]:
                continue
            if (dir_dist != 0 and direction != next_dir and dir_dist < min_dist) or (direction == next_dir and dir_dist == max_dist):
                continue

            next_node = (nr, nc, next_dir, 1 + (dir_dist if direction == next_dir else 0))
            next_distance = current_distance + grid[nr][nc]

            if next_distance < distances.get(next_node, sys.maxsize):
                distances[next_node] = next_distance
                heapq.heappush(priority_queue, (next_distance, next_node))

    return min(distance for (r, c, _, dir_dist), distance in distances.items() if r == rows - 1 and c == cols - 1 and min_dist <= dir_dist <= max_dist)


def part1(grid):
    return solve(grid, 1, 3)

def part2(grid):
    return solve(grid, 4, 10)

grid = parse_input(inp)

print('part1:', part1(grid))
print('part2:', part2(grid))
