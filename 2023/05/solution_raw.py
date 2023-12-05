import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())

seeds = [int(n) for n in inp[0].split(': ')[1].split(' ')]

maps = []
for r, row in enumerate(inp[2:]):
    if 'map' in row:
        maps.append([])
    elif row.strip() != '':
        [dest, src, rng] = [int(n) for n in row.split(' ')]
        maps[-1].append((src, dest, rng))

min_val = 100000000000000
for seed in seeds:
    val = seed
    for m in maps:
        for (src, dest, rng) in m:
            if val >= src and val < src + rng:
                val = dest + val - src
                break
    min_val = min(val, min_val)

print(min_val)


seed_ranges = zip(seeds[::2], seeds[1::2])

def apply_range(m, cur_rng):
    res = []
    for (src, dest, rng) in m:
        src_end = src + rng
        not_mapped = []
        while cur_rng:
            (start, end) = cur_rng.pop()
            before = (start, min(end, src))
            current = (max(src, start), min(src_end, end))
            after = (max(start, src_end), end)
            if before[0] < before[1]:
                not_mapped.append(before)
            if after[0] < after[1]:
                not_mapped.append(after)
            if current[0] < current[1]:
                res.append((current[0] - src + dest, current[1] - src + dest))
        cur_rng = not_mapped
    return res + cur_rng

min_val = 100000000000000
for seed, rng in seed_ranges:
    cur_range = [(seed, seed + rng)]
    for m in maps:
        cur_range = apply_range(m, cur_range)
    min_val = min(min_val, min(cur_range)[0])

print(min_val)
