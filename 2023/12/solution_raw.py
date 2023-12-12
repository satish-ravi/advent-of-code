import sys
import functools

inp = list(l.strip() for l in sys.stdin.readlines())

def get_all(st):
    if st == '':
        return ['']

    nx = get_all(st[1:])
    if st[0] != '?':
        return [st[0] + n for n in nx]
    else:
        return ['.' + n for n in nx] + ['#' + n for n in nx]

def matches(ar, n):
    val = []
    c = 0
    for x in ar:
        if x == '.':
            if c > 0:
                val.append(c)
                c = 0
            continue
        c += 1
    if c > 0:
        val.append(c)
    return n == val

# ans = 0
# for r in inp:
#     ar, num = r.split()
#     n = [int(x) for x in num.split(',')]
#     all_ar = get_all(ar)
#     ans += sum([1 for x in all_ar if matches(x, n)])
# print(ans)

@functools.lru_cache(maxsize=None)
def solve(s, nums, cur):
    if s == '':
        if len(nums) == 0 and cur is None or len(nums) == 1 and nums[0] == cur:
            return 1
        return 0
    rem_hash = len([x for x in s if x == '#'])
    rem_unknown = len([x for x in s if x == '?'])

    if rem_hash + rem_unknown + (cur or 0) < sum(nums) or rem_hash > sum(nums):
        return 0
    if cur:
        if cur == nums[0]:
            if s[0] in ['?', '.']:
                return solve(s[1:], nums[1:], None)
            else:
                return 0
        else:
            if s[0] in ['?', '#']:
                return solve(s[1:], nums, cur + 1)
            else:
                return 0
    else:
        if s[0] == '.':
            return solve(s[1:], nums, None)
        elif s[0] == '#':
            if not nums:
                return 0
            return solve(s[1:], nums, 1)
        else:
            return solve(s[1:], nums, None) + (solve(s[1:], nums, 1) if nums else 0)


ans = 0
for r in inp:
    ar, num = r.split()
    n = tuple([int(x) for x in num.split(',')])
    ans += solve(ar, n, None)
print(ans)

ans = 0
for r in inp:
    ar, num = r.split()
    n = tuple([int(x) for x in num.split(',')])
    ans += solve(((ar + '?') * 5)[:-1], n * 5, None)
print(ans)
