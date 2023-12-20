import sys
from collections import deque
import math
inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0

ff = {}
cnj = {}
b = None

for r, row in enumerate(inp):
    l, r = row.split(' -> ')
    if l[0] == '%':
        ff[l[1:]] = r.split(', ')
    elif l[0] == '&':
        cnj[l[1:]] = r.split(', ')
    else:
        b = r.split(', ')

ffs = {f: False for f in ff.keys()}
cnjs = {cn: {} for cn in cnj.keys()}

for f, res in ff.items():
    for r in res:
        if r in cnjs.keys():
            cnjs[r][f] = 'l'

for cn, res in cnj.items():
    for r in res:
        if r in cnjs.keys():
            cnjs[r][cn] = 'l'

lp, hp = 0, 0

for _ in range(1000):
    q = deque([('l', o, 'broadcaster') for o in b])
    lp += 1

    while q:
        p, m, src = q.popleft()
        if p == 'l':
            lp += 1
        else:
            hp += 1
        if m in ff:
            if p == 'h':
                continue
            q.extend([('l' if ffs[m] else 'h', nm, m) for nm in ff[m]])
            ffs[m] = not ffs[m]
        elif m in cnj:
            cnjs[m][src] = p
            q.extend([('l' if all(v == 'h' for v in cnjs[m].values()) else 'h', nm, m) for nm in cnj[m]])

print(lp * hp)

ffs = {f: False for f in ff.keys()}
cnjs = {cn: {} for cn in cnj.keys()}

for f, res in ff.items():
    for r in res:
        if r in cnjs.keys():
            cnjs[r][f] = 'l'

for cn, res in cnj.items():
    for r in res:
        if r in cnjs.keys():
            cnjs[r][cn] = 'l'

btn = 0
found = False

rx_in = [cn for cn, v in cnj.items() if v == ['rx']][0]

lo_indices = {m: None for m in cnjs[rx_in].keys()}

while any(v == None for v in lo_indices.values()):
    btn += 1

    q = deque([('l', o, 'broadcaster') for o in b])

    while q:
        p, m, src = q.popleft()
        if p == 'l' and m in lo_indices:
            lo_indices[m] = btn
        if m in ff:
            if p == 'h':
                continue
            q.extend([('l' if ffs[m] else 'h', nm, m) for nm in ff[m]])
            ffs[m] = not ffs[m]
        elif m in cnj:
            cnjs[m][src] = p
            q.extend([('l' if all(v == 'h' for v in cnjs[m].values()) else 'h', nm, m) for nm in cnj[m]])

def lcm_of_list(numbers):
    if len(numbers) == 0:
        raise ValueError("List must contain at least one number.")

    result = numbers[0]

    for num in numbers[1:]:
        result = abs(result * num) // math.gcd(result, num)

    return result

print(lcm_of_list(list(lo_indices.values())))

