import sys
from collections import deque
from itertools import permutations

Coord = tuple[int, int, int]
Scanner = set[Coord]

ORIENTATIONS = set()
DIMENSIONS = 3

for x in [-1, 1]:
    for y in [-2, 2]:
        for z in [-3, 3]:
            for perm in permutations((x, y, z)):
                ORIENTATIONS.add(perm)


def read_input() -> list[Scanner]:
    scanners = []
    for l in sys.stdin.readlines():
        line = l.strip()
        if "scanner" in line:
            scanner = set()
            scanners.append(scanner)
        elif line:
            scanner.add(tuple([int(v) for v in line.split(",")]))
    return scanners


def get_offset(scanner1: Scanner, scanner2: Scanner, num_matching: int = 12) -> Coord:
    for b1 in scanner1:
        for b2 in scanner2:
            offset = tuple(b1[i] - b2[i] for i in range(DIMENSIONS))
            s2_offset = apply_offset(scanner2, offset)
            if len(scanner1.intersection(s2_offset)) >= num_matching:
                return offset


def apply_orientation(scanner: Scanner, orientation: Coord) -> Scanner:
    oriented_scanner = []
    for Coord in scanner:
        oriented_scanner.append(
            tuple(
                Coord[abs(orientation[i]) - 1] * orientation[i] // abs(orientation[i])
                for i in range(DIMENSIONS)
            )
        )
    return oriented_scanner


def memoize_orientations(f):
    memory = {}

    def inner(idx: int, scanner: Scanner) -> list[Scanner]:
        if idx not in memory:
            memory[idx] = f(idx, scanner)
        return memory[idx]

    return inner


@memoize_orientations
def get_orientations(idx: int, scanner: Scanner) -> list[Scanner]:
    all_orientations = []
    for orientation in ORIENTATIONS:
        all_orientations.append((orientation, apply_orientation(scanner, orientation)))
    return all_orientations


def apply_offset(scanner: Scanner, offset: Coord) -> Scanner:
    offsetted_scanner = set()
    for Coord in scanner:
        offsetted_scanner.add(tuple(Coord[i] + offset[i] for i in range(DIMENSIONS)))
    return offsetted_scanner


def build_scanner_orientation_and_offset(
    scanners: list[Scanner],
) -> dict[int, tuple[Scanner, Coord]]:
    scanner_queue = deque()
    scanner_queue.append(scanners[0])
    final_scanners = {0: (scanners[0], (0, 0, 0))}

    while len(final_scanners.keys()) < len(scanners):
        assert scanner_queue, "Not all scanners connected"
        current_scanner = scanner_queue.popleft()
        for idx in set(range(len(scanners))) - set(final_scanners.keys()):
            for _, oriented_scanner in get_orientations(idx, scanners[idx]):
                offset = get_offset(current_scanner, oriented_scanner)
                if offset:
                    final_scanner = apply_offset(oriented_scanner, offset)
                    final_scanners[idx] = (final_scanner, offset)
                    scanner_queue.append(final_scanner)
                    break

    return final_scanners


def get_beacons_and_scanners(
    scanners: list[Scanner],
) -> tuple[list[Coord], list[Coord]]:
    result = build_scanner_orientation_and_offset(scanners)
    beacons = set()
    scanner_locations = []

    for _, (scanner, offset) in result.items():
        beacons = beacons.union(scanner)
        scanner_locations.append(offset)

    return list(beacons), scanner_locations


def part1(beacons: list[Coord]) -> int:
    return len(beacons)


def part2(scanner_locations: list[Coord]) -> int:
    max_distance = -1
    for i in range(len(scanner_locations) - 1):
        for j in range(i, len(scanner_locations)):
            distance = sum(
                abs(scanner_locations[i][x] - scanner_locations[j][x])
                for x in range(DIMENSIONS)
            )
            if distance > max_distance:
                max_distance = distance
    return max_distance


scanners = read_input()
beacons, scanner_locations = get_beacons_and_scanners(scanners)

print("part1:", part1(beacons))
print("part2:", part2(scanner_locations))
