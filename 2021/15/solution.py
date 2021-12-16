from collections import defaultdict
from copy import Error
import sys
import heapq


def read_input() -> list[list[int]]:
    return [[int(c) for c in l.strip()] for l in sys.stdin.readlines()]


def repeat_grid(grid: list[list[int]], repeat: int) -> list[list[int]]:
    new_grid = [[None for _ in range(5 * len(grid))] for _ in range(5 * len(grid))]

    for r in range(len(new_grid)):
        for c in range(len(new_grid[0])):
            dr = r // len(grid)
            dc = c // len(grid[0])
            orig_r = r % len(grid)
            orig_c = c % len(grid[0])
            new_grid[r][c] = grid[orig_r][orig_c] + dr + dc
            if new_grid[r][c] >= 10:
                new_grid[r][c] -= 9

    return new_grid


def find_shortest_path(grid: list[list[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)
    visited = set()
    queue = []

    costs = defaultdict(lambda: float("inf"))
    costs[start] = 0
    heapq.heappush(queue, (0, start))

    while queue:
        _, node = heapq.heappop(queue)
        visited.add(node)
        if node == end:
            return costs[end]
        i, j = node

        for (di, dj) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            ai = i + di
            aj = j + dj

            if 0 <= ai < len(grid) and 0 <= aj < len(grid[0]):
                if (ai, aj) in visited:
                    continue
                new_cost = costs[(i, j)] + grid[ai][aj]
                if new_cost < costs[(ai, aj)]:
                    costs[(ai, aj)] = new_cost
                    heapq.heappush(queue, (new_cost, (ai, aj)))

    raise Error("no path found")


grid = read_input()
print("part1:", find_shortest_path(grid))
print("part2:", find_shortest_path(repeat_grid(grid, 5)))
