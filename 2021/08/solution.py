from collections import defaultdict
import itertools
import sys
from typing import Iterable, Union

NUMBER_TO_DISPLAY = [
    [0, 1, 2, 4, 5, 6],  # abcefg
    [2, 5],  # cf
    [0, 2, 3, 4, 6],  # acdeg
    [0, 2, 3, 5, 6],  # acdfg
    [1, 2, 3, 5],  # bcdf
    [0, 1, 3, 5, 6],  # abdfg
    [0, 1, 3, 4, 5, 6],  # abdefg
    [0, 2, 5],  # acf
    [0, 1, 2, 3, 4, 5, 6],  # abcdefg
    [0, 1, 2, 3, 5, 6],  # abcdfg
]

LENGTH_TO_NUMBERS = defaultdict(list)
for i, positions in enumerate(NUMBER_TO_DISPLAY):
    LENGTH_TO_NUMBERS[len(positions)].append(i)


def read_input() -> tuple[str, str]:
    return list(l.strip().split(" | ") for l in sys.stdin.readlines())


def part1(inp: tuple[str, str]) -> int:
    result = 0
    for _, display in inp:
        for item in display.split():
            if len(set(item)) in [2, 3, 4, 7]:
                result += 1
    return result


def sorted_chars(chars: Union[str, Iterable]) -> str:
    return "".join(sorted(chars))


def part2(inp: tuple[str, str]) -> int:
    all_options = []
    for combo in itertools.permutations(set("abcdefg")):
        all_options.append(
            [sorted_chars(combo[i] for i in item) for item in NUMBER_TO_DISPLAY]
        )

    result = 0

    for all_numbers, display in inp:
        numbers_set = set(sorted_chars(x) for x in all_numbers.split())
        found_option = None
        for option in all_options:
            if numbers_set == set(option):
                found_option = option
                break
        num = 0
        for display_item in (sorted_chars(x) for x in display.split()):
            num = num * 10 + found_option.index(display_item)
        result += num
    return result


def part2_optimal(inp: tuple[str, str]) -> int:
    result = 0
    for all_numbers, display in inp:
        possibilities = defaultdict(list)
        for item in all_numbers.split():
            chars = set(item)
            for choice in LENGTH_TO_NUMBERS[len(chars)]:
                possibilities[choice].append(chars)

        # extract known
        cf = possibilities[1][0]
        acf = possibilities[7][0]
        bcdf = possibilities[4][0]

        # top(a) will be in 7 but not 1
        a = list(acf - cf)[0]
        g_choices = set("abcdefg")

        # only top(a) and bottom(g) are common in these numbers
        for i in [0, 2, 3, 5, 6, 9]:
            for possibility in possibilities[i]:
                g_choices = g_choices.intersection(possibility)
        g = list(g_choices - set([a]))[0]

        # 9 is 4 + top(a) and bottom(g)
        abcdfg = bcdf.union(set([a, g]))
        possibilities[9] = [abcdfg]
        e = list(set("abcdefg") - abcdfg)[0]

        # filter numbers with length 5
        possibilities[3] = [x for x in possibilities[3] if cf.issubset(x)]
        possibilities[2] = [x for x in possibilities[2] if e in x]
        possibilities[5] = [
            x
            for x in possibilities[5]
            if x != possibilities[3][0] and x != possibilities[2][0]
        ]

        # filter numbers with length 6
        possibilities[6] = [possibilities[5][0].union([e])]
        possibilities[0] = [
            x
            for x in possibilities[0]
            if x != possibilities[6][0] and x != possibilities[9][0]
        ]

        final = {}
        for (num, option) in possibilities.items():
            final[sorted_chars(option[0])] = num
        num = 0
        for display_item in (sorted_chars(x) for x in display.split()):
            num = num * 10 + final[display_item]
        result += num

    return result


inp = read_input()
print("part1:", part1(inp))
print("part2:", part2(inp))
print("part2_opt:", part2_optimal(inp))
