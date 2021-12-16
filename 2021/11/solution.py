import sys
from copy import deepcopy


def read_input() -> list[list[int]]:
    return [[int(c) for c in line.strip()] for line in sys.stdin.readlines()]


def get_adjacent(i: int, j: int, r: int, c: int) -> list[tuple[int, int]]:
    result = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            ai = i + di
            aj = j + dj
            if not (di == 0 and dj == 0) and ai >= 0 and ai < r and aj >= 0 and aj < c:
                result.append((ai, aj))
    return result


def increment_and_flash(octopuses: list[list[int]]) -> None:
    r = len(octopuses)
    c = len(octopuses[0])
    flashed = set()
    for i in range(r):
        for j in range(c):
            octopuses[i][j] += 1
            if octopuses[i][j] == 10:
                flashed.add((i, j))

    total_flashed = 0
    while len(flashed):
        total_flashed += len(flashed)
        new_flashed = set()
        for (i, j) in flashed:
            octopuses[i][j] = 0
            for (ai, aj) in get_adjacent(i, j, r, c):
                if (
                    (ai, aj) in flashed
                    or (ai, aj) in new_flashed
                    or octopuses[ai][aj] == 0
                ):
                    continue
                octopuses[ai][aj] += 1
                if octopuses[ai][aj] >= 10:
                    new_flashed.add((ai, aj))
        flashed = new_flashed

    return total_flashed


def part1(inp: list[list[int]]) -> int:
    octopuses = deepcopy(inp)
    result = 0
    for _ in range(100):
        result += increment_and_flash(octopuses)
    return result


def part2(inp: list[list[int]]) -> int:
    octopuses = deepcopy(inp)
    flash_num = 0
    total = len(inp) * len(inp[0])
    while True:
        flash_num += 1
        if increment_and_flash(octopuses) == total:
            return flash_num


inp = read_input()
print("part1:", part1(inp))
print("part2:", part2(inp))
