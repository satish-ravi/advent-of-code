import sys


def read_input() -> list[list[int]]:
    inp = []
    for line in sys.stdin.readlines():
        inp.append([int(x) for x in line.strip()])
    return inp


def get_adjacent(i: int, j: int, r: int, c: int) -> list[tuple[int, int]]:
    adjacent = []
    for (di, dj) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ai = i + di
        aj = j + dj
        if ai < 0 or aj < 0 or ai >= r or aj >= c:
            continue
        adjacent.append((ai, aj))
    return adjacent


def get_low_points(inp: list[list[int]]) -> list[tuple[int, int]]:
    r = len(inp)
    c = len(inp[0])
    result = []
    for i in range(r):
        for j in range(c):
            if all(inp[ai][aj] > inp[i][j] for (ai, aj) in get_adjacent(i, j, r, c)):
                result.append((i, j))
    return result


def part1(inp: list[list[int]]) -> int:
    return sum(inp[i][j] + 1 for (i, j) in get_low_points(inp))


def part2(inp: list[list[int]]) -> int:
    basins = []
    for (i, j) in get_low_points(inp):
        basin = set([(i, j)])
        queue = [(i, j)]
        while len(queue):
            ci, cj = queue.pop()
            for (ai, aj) in get_adjacent(ci, cj, len(inp), len(inp[0])):
                if (ai, aj) not in basin and inp[ai][aj] != 9:
                    basin.add((ai, aj))
                    queue.append((ai, aj))
        basins.append(basin)
    sorted_basins = sorted(basins, key=lambda basin: -len(basin))
    result = 1
    for i in range(3):
        result *= len(sorted_basins[i])
    return result


inp = read_input()
print("part1:", part1(inp))
print("part2:", part2(inp))
