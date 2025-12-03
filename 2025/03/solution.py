import sys
from collections import Counter

inp = list(l.strip() for l in sys.stdin.readlines())

def parse_input(inp):
    return [[int(n) for n in line] for line in inp]

def get_best(nums, l):
    if l == 1:
        return max(nums)
    best, best_idx = 0, -1
    for i in range(len(nums)-l+1):
        if nums[i] > best:
            best, best_idx = nums[i], i

    next_best = get_best(nums[best_idx+1:], l-1)

    return best * (10 ** (l-1)) + next_best


def solve(all_nums, l):
    total = 0
    for nums in all_nums:
        total += get_best(nums, l)
    return total


def part1(all_nums):
    return solve(all_nums, 2)

def part2(all_nums):
    return solve(all_nums, 12)

all_nums = parse_input(inp)
print('part1:', part1(all_nums))
print('part2:', part2(all_nums))
