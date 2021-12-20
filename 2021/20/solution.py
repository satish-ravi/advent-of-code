import sys
from collections import defaultdict, deque
from itertools import permutations
from typing import Optional

Image = dict[tuple[int, int], bool]


def read_input() -> tuple[str, Image]:
    lines = sys.stdin.readlines()

    algo = lines[0].strip()
    image = defaultdict(lambda: False)

    for (r, line) in enumerate(lines[2:]):
        for c, char in enumerate(line.strip()):
            image[(r, c)] = char == "#"

    return algo, image


def get_neighbors_number(image: Image, r: int, c: int) -> int:
    num_bin = ""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            num_bin += "1" if image[(r + dr, c + dc)] else "0"
    return int(num_bin, 2)


def enhance_image(algo: str, image: Image) -> Image:
    keys = image.keys()

    rows = [k[0] for k in keys]
    cols = [k[1] for k in keys]

    start_row = min(rows) - 1
    end_row = max(rows) + 1
    start_col = min(cols) - 1
    end_col = max(cols) + 1

    new_default = get_neighbors_number(image, start_row - 10, start_col - 10)

    enhanced_image = defaultdict(lambda: algo[new_default] == "#")

    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            enhanced_image[(r, c)] = algo[get_neighbors_number(image, r, c)] == "#"

    return enhanced_image


def count_lights(image: Image) -> int:
    return len([val for val in image.values() if val])


def get_enhanced_count(algo: str, image: Image, times: int) -> int:
    enhanced_image = image
    for _ in range(times):
        enhanced_image = enhance_image(algo, enhanced_image)
    return count_lights(enhanced_image)


algo, image = read_input()

print("part1:", get_enhanced_count(algo, image, 2))
print("part2:", get_enhanced_count(algo, image, 50))
