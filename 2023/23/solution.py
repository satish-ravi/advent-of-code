import sys

inp = list(l.strip() for l in sys.stdin.readlines())

DIRECTION_OPTIONS = {
    '.': [(0, 1), (1, 0), (0, -1), (-1, 0)],
    '<': [(0, -1)],
    '>': [(0, 1)],
    '^': [(-1, 0)],
    'v': [(1, 0)],
}

def parse_input(inp):
    rows = len(inp)
    cols = len(inp[0])

    start = None
    end = None
    for c in range(cols):
        if inp[0][c] == '.':
            if start:
                raise Exception(f'multiple starts at {start},{0, c}')
            start = (0, c)
        if inp[rows-1][c] == '.':
            if end:
                raise Exception(f'multiple starts at {start},{rows-1, c}')
            end = (rows-1, c)
    return inp, start, end

def get_neighbors(grid, r, c, only_down_on_slop):
    rows = len(grid)
    cols = len(grid[0])
    neighbors = []
    for dr, dc in DIRECTION_OPTIONS[grid[r][c] if only_down_on_slop else '.']:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            neighbors.append((nr, nc))
    return neighbors


def solve(grid, start, end, only_down_on_slop):
    hubs = {start: {}, end: {}}
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '#' and len(get_neighbors(grid, r, c, only_down_on_slop)) > 2:
                hubs[(r, c)] = {}

    def hub_neighbors(hub, hub_next):
        if hub_next in hubs:
            return {hub_next: 1}
        visited = {hub}
        connected_hubs = {}
        stack = [(hub_next, 1)]
        while stack:
            current, distance = stack.pop()
            if current in visited:
                continue
            if current in hubs:
                connected_hubs[current] = distance
                continue
            visited.add(current)
            r, c = current
            stack.extend([(neighbor, distance + 1) for neighbor in get_neighbors(grid, r, c, only_down_on_slop)])
        return connected_hubs

    for hub, connected in hubs.items():
        r, c = hub
        for hub_next in get_neighbors(grid, r, c, only_down_on_slop):
            for connected_hub, distance in hub_neighbors(hub, hub_next).items():
                connected[connected_hub] = max(distance, connected.get(connected_hub, distance))

    result = 0
    stack = [(start, set([start]), 0)]
    while stack:
        hub, visited, distance = stack.pop()
        for connected_hub, connected_distance in hubs[hub].items():
            next_distance = distance + connected_distance
            if connected_hub in visited:
                continue
            if connected_hub == end:
                result = max(result, next_distance)
                continue
            stack.append((connected_hub, visited | {connected_hub}, next_distance))
    return result

grid, start, end = parse_input(inp)
print('part1:', solve(grid, start, end, True))
print('part2:', solve(grid, start, end, False))
