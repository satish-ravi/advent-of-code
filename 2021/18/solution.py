import json
import sys
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class LeafNode:
    parent: tuple
    parent_idx: int
    grand_parent: tuple
    grand_parent_idx: int


def read_input():
    return [json.loads(l.strip()) for l in sys.stdin.readlines()]


def add(p1, p2):
    return [p1, p2]


def get_magnitude(pair):
    if type(pair) == int:
        return pair
    return 3 * get_magnitude(pair[0]) + 2 * get_magnitude(pair[1])


def get_pair_to_split(pair):
    if type(pair) == int:
        return None, None
    if type(pair[0]) == int and pair[0] >= 10:
        return (pair, 0)
    left = get_pair_to_split(pair[0])
    if left[0]:
        return left
    if type(pair[1]) == int and pair[1] >= 10:
        return (pair, 1)
    return get_pair_to_split(pair[1])


def split(pair):
    pair_to_split, index = get_pair_to_split(pair)
    if pair_to_split:
        val = pair_to_split[index]
        pair_to_split[index] = [val // 2, val - val // 2]
        return True
    return False


def construct_by_index(pair, parent, parent_idx, result):
    if type(pair[0]) == int:
        left = pair[0], len(result)
        result.append(LeafNode(pair, 0, parent, parent_idx))
    else:
        left = construct_by_index(pair[0], pair, 0, result)
    if type(pair[1]) == int:
        right = pair[1], len(result)
        result.append(LeafNode(pair, 1, parent, parent_idx))
    else:
        right = construct_by_index(pair[1], pair, 1, result)
    return [left, right]


def get_pair_to_explode(pair, level=1):
    if type(pair) == int:
        return None
    if level == 4:
        if type(pair[0]) == list:
            return pair[0]
        if type(pair[1]) == list:
            return pair[1]
    return get_pair_to_explode(pair[0], level + 1) or get_pair_to_explode(
        pair[1], level + 1
    )


def explode(pair):
    pair_by_index = []
    pair_with_index = construct_by_index(pair, None, None, pair_by_index)

    pair_to_explode = get_pair_to_explode(pair_with_index)

    if not pair_to_explode:
        return False

    left_val, left_idx = pair_to_explode[0]
    right_val, right_idx = pair_to_explode[1]

    if left_idx > 0:
        left_node = pair_by_index[left_idx - 1].parent
        left_node[pair_by_index[left_idx - 1].parent_idx] += left_val

    if right_idx < len(pair_by_index) - 1:
        right_node = pair_by_index[right_idx + 1].parent
        right_node[pair_by_index[right_idx + 1].parent_idx] += right_val

    # setting exploded to 0
    parent = pair_by_index[left_idx].grand_parent
    parent[pair_by_index[left_idx].grand_parent_idx] = 0

    return True


def reduce(pair):
    while True:
        while True:
            if not explode(pair):
                break
        if not split(pair):
            break


def part1(pairs):
    pairs = deepcopy(pairs)
    pair = pairs[0]

    for next_pair in pairs[1:]:
        pair = add(pair, next_pair)
        reduce(pair)
    return get_magnitude(pair)


def part2(pairs):
    max = -1
    pairs = deepcopy(pairs)

    for i in range(len(pairs)):
        for j in range(len(pairs)):
            if i == j:
                continue
            pair = add(deepcopy(pairs[i]), deepcopy(pairs[j]))
            reduce(pair)
            mg = get_magnitude(pair)
            if mg > max:
                max = mg
    return max


inp = read_input()
print("part1:", part1(inp))
print("part2:", part2(inp))
