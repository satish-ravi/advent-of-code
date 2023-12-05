import sys
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass
class MapEntry:
    src: int
    dest: int
    size: int

    @property
    def src_end(self):
        return self.src + self.size

    def apply_val(self, val):
        if self.src <= val < self.src + self.size:
            return val + self.dest - self.src
        return None

    def apply_ranges(self, ranges):
        not_mapped = []
        mapped = []
        for rng in ranges:
            (start, end) = rng
            before = (start, min(end, self.src))
            current = (max(self.src, start), min(self.src_end, end))
            after = (max(start, self.src_end), end)
            if before[0] < before[1]:
                not_mapped.append(before)
            if after[0] < after[1]:
                not_mapped.append(after)
            if current[0] < current[1]:
                mapped.append((current[0] - self.src + self.dest, current[1] - self.src + self.dest))
        return mapped, not_mapped

@dataclass
class Map:
    entries: list[MapEntry]

    def apply_val(self, val):
        for entry in self.entries:
            res = entry.apply_val(val)
            if res is not None:
                return res
        return val

    def apply_ranges(self, ranges):
        result_rng = []
        not_mapped = ranges
        for entry in self.entries:
            mapped, not_mapped = entry.apply_ranges(not_mapped)
            if mapped:
                result_rng.extend(mapped)
        return result_rng + (not_mapped if not_mapped else [])


def parse_input(inp):
    seeds = [int(n) for n in inp[0].split(': ')[1].split(' ')]
    maps = []
    current_map_entries = []
    for row in inp[3:]:
        if 'map' in row:
            continue
        elif row.strip() == '':
            maps.append(Map(current_map_entries))
            current_map_entries = []
        else:
            [dest, src, size] = [int(n) for n in row.split(' ')]
            current_map_entries.append(MapEntry(src, dest, size))
    if current_map_entries:
        maps.append(Map(current_map_entries))
    return seeds, maps

def part1(seeds, maps):
    locations = []
    for seed in seeds:
        val = seed
        for mp in maps:
            val = mp.apply_val(val)
        locations.append(val)
    return min(locations)


def part2(seeds, maps):
    locations = []
    for seed_start, size in zip(seeds[::2], seeds[1::2]):
        ranges = [(seed_start, seed_start + size)]
        for mp in maps:
            ranges = mp.apply_ranges(ranges)
        locations.append(min(ranges)[0])
    return min(locations)

seeds, maps = parse_input(inp)

print('part1:', part1(seeds, maps))
print('part2:', part2(seeds, maps))
