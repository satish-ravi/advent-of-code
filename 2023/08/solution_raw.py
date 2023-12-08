import sys
import re
import math

inp = list(l.strip() for l in sys.stdin.readlines())

mapping = {}

for r, row in enumerate(inp[2:]):
    k, v = row.split(' = ')
    l, r = v[1:-1].split(', ')
    mapping[k] = {'L': l, 'R': r}

def get_next():
    i = 0
    while True:
        yield inp[0][i]
        i = (i + 1) % len(inp[0])
ans = 0
val = 'AAA'
getter = get_next()
while val != 'ZZZ':
    val = mapping[val][next(getter)]
    ans += 1

print(ans)

def solve(val):
    getter = get_next()
    ans = 0
    while val[-1] != 'Z':
        val = mapping[val][next(getter)]
        ans += 1
    return ans

individual_ans = [solve(k) for k in mapping.keys() if k[-1] == 'A']

def lcm_of_list(numbers):
    if len(numbers) == 0:
        raise ValueError("List must contain at least one number.")

    result = numbers[0]

    for num in numbers[1:]:
        result = abs(result * num) // math.gcd(result, num)

    return result

print(lcm_of_list(individual_ans))
