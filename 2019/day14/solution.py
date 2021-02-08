#!/usr/bin/env python3

import sys
from collections import defaultdict


def ore_required(fuel=1):
    chem_needs = defaultdict(int, {"FUEL": fuel})
    chem_have = defaultdict(int)
    ore = 0

    while chem_needs:
        item = list(chem_needs.keys())[-1]
        if chem_needs[item] <= chem_have[item]:
            chem_have[item] -= chem_needs[item]
            del chem_needs[item]
            continue

        num_needed = chem_needs[item] - chem_have[item]
        del chem_have[item]
        del chem_needs[item]
        num_produced = reactions[item]["out"]

        if (num_needed // num_produced) * num_produced == num_needed:
            num_reactions = num_needed // num_produced
        else:
            num_reactions = (num_needed // num_produced) + 1
        # print(num_needed, num_produced, num_reactions)

        chem_have[item] += (num_reactions * num_produced) - num_needed
        for chem in reactions[item]["in"]:
            if chem == "ORE":
                ore += reactions[item]["in"][chem] * num_reactions
            else:
                chem_needs[chem] += reactions[item]["in"][chem] * num_reactions
        # print(f'{ore} {chem_needs} {chem_have}')

    return ore


with open(sys.argv[1], "r") as f:
    reaction_lines = list(map(str.strip, f.readlines()))

reactions = {}
for r in reaction_lines:
    i, o = r.split(" => ")
    o_num, o_chem = o.split(" ")
    inputs = {}
    for in_str in i.split(", "):
        i_num, i_chem = in_str.split(" ")
        inputs[i_chem] = int(i_num)
    reactions[o_chem] = {"out": int(o_num), "in": inputs}


print(f"Part 1: {ore_required()}")

low = 1e12 // ore_required()
high = 10 * low

while ore_required(high) < 1e12:
    low = high
    high = 10 * low

while low < high - 1:
    mid = (low + high) // 2
    ore = ore_required(mid)
    if ore < 1e12:
        low = mid
    elif ore > 1e12:
        high = mid
    else:
        break

print(f"Part 2: {int(mid)}")
