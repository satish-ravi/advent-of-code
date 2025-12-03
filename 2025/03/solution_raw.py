import sys

inp = list(l.strip() for l in sys.stdin.readlines())

def part1(inp):
    ans = 0
    for line in inp:
        cur_max = 0
        for i in range(len(line)):
            for j in range(i+1, len(line)):
                cur = int(line[i] + line[j])
                if cur > cur_max:
                    cur_max = cur
        ans += cur_max
    return ans


def get_best(nums, l):
    if l == 1:
        return max(nums)
    best, best_idx = 0, -1
    for i in range(len(nums)-l+1):
        if nums[i] > best:
            best, best_idx = nums[i], i

    next_best = get_best(nums[best_idx+1:], l-1)

    return best * (10 ** (l-1)) + next_best


def part2(inp):
    ans = 0
    L = 12
    for line in inp:
        as_num = [int(n) for n in line]
        ans += get_best(as_num, L)
    return ans

print('part1:', part1(inp))
print('part2:', part2(inp))
