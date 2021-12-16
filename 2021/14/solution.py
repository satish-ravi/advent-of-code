import sys
from collections import defaultdict


def read_input() -> tuple[str, dict[str, str]]:
    inp = [l.strip() for l in sys.stdin.readlines()]
    polymer = inp[0]
    pair_rules = {}
    for item in inp[2:]:
        lhs, rhs = item.split(" -> ")
        pair_rules[lhs] = rhs

    return polymer, pair_rules


def polymerize(polymer: str, pair_rules: dict[str, str], n_steps: int) -> int:
    p = polymer
    for _ in range(n_steps):
        new_p = ""
        for i in range(len(p) - 1):
            new_p += p[i] + pair_rules[p[i : i + 2]]
        new_p += p[-1]
        p = new_p

    c = defaultdict(int)
    for ch in p:
        c[ch] += 1
    return max(c.values()) - min(c.values())


def polymerize_optimal(polymer: str, pair_rules: dict[str, str], n_steps: int) -> int:
    p = polymer
    count_pairs = defaultdict(int)
    for i in range(len(p) - 1):
        count_pairs[p[i : i + 2]] += 1

    for _ in range(n_steps):
        new_pairs = defaultdict(int)
        for pair, count in count_pairs.items():
            p1, p2 = list(pair)
            result = pair_rules[pair]
            new_pairs[p1 + result] += count
            new_pairs[result + p2] += count
        count_pairs = new_pairs

    counter = defaultdict(int)
    for pair, count in count_pairs.items():
        counter[pair[0]] += count
        counter[pair[1]] += count

    counter[polymer[0]] += 1
    counter[polymer[-1]] += 1

    final_counter = {}
    for ch, count in counter.items():
        final_counter[ch] = count // 2

    return max(final_counter.values()) - min(final_counter.values())


polymer, pair_rules = read_input()
print("part1:", polymerize_optimal(polymer, pair_rules, 10))
print("part2:", polymerize_optimal(polymer, pair_rules, 40))
