import sys

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    intervals = []
    ingredients = []

    intervals_done = False
    for row in inp:
        if row == '':
            intervals_done = True
            continue
        if intervals_done:
            ingredients.append(int(row))
        else:
            intervals.append([int(n) for n in row.split('-')])
    return intervals, ingredients

def part1(intervals, ingredients):
    ans = 0
    for ingredient in ingredients:
        for interval in intervals:
            if interval[0] <= ingredient <= interval[1]:
                ans += 1
                break
    return ans

def part2(intervals, _):
    sorted_intervals = sorted(intervals)

    merged_intervals = []
    for interval in sorted_intervals:
        if not merged_intervals or merged_intervals[-1][1] < interval[0]:
            merged_intervals.append(interval)
        else:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], interval[1])

    ans = 0
    for interval in merged_intervals:
        ans += interval[1] - interval[0] + 1
    return ans


intervals, ingredients = parse_input(inp)
print('part1:', part1(intervals, ingredients))
print('part2:', part2(intervals, ingredients))
