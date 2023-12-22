import sys
from collections import deque
import math
import functools
inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0

rs = len(inp)
cs = len(inp[0])

bs = []

for r, row in enumerate(inp):
    s, e = row.split('~')
    sp = tuple([int(c) for c in s.split(',')])
    ep = tuple([int(c) for c in e.split(',')])
    bs.append((sp, ep) if ep[-1] >= sp[-1] else (ep, sp))

sbs = sorted(bs, key=lambda b: min(b[0][-1], b[1][-1]))

fallen = []
occupied = {}

for b in sbs:
    x1, x2 = b[0][0], b[1][0]
    y1, y2 = b[0][1], b[1][1]
    z1, z2 = b[0][2], b[1][2]
    if z1 == 1:
        fallen.append(b)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(z1, z2 + 1):
                    if (x, y, z) in occupied:
                        print(b, x, y, z)
                        raise Exception('impossible1')
                    occupied[(x, y, z)] = b
        continue
    zc = z1
    stop = False
    while zc > 1 and not stop:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if (x, y, zc-1) in occupied:
                    stop = True
                    break
            if stop:
                break
        if stop:
            break
        zc -= 1
    fb = ((x1, y1, zc), (x2, y2, z2 - z1 + zc))
    fallen.append(fb)
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for z in range(zc, z2 - z1 + zc + 1):
                if (x, y, z) in occupied:
                    raise Exception('impossible2')
                occupied[(x, y, z)] = fb
print(len(occupied))
only_connected = {b: set([]) for b in fallen}
connected = {b: set([]) for b in fallen}
supported = {b: set([]) for b in fallen}

for b in fallen:
    x1, x2 = b[0][0], b[1][0]
    y1, y2 = b[0][1], b[1][1]
    z1, z2 = b[0][2], b[1][2]

    assert z1 <= z2

    cbs = set([])
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if (x, y, z2 + 1) in occupied:
                cbs.add(occupied[(x, y, z2 + 1)])

    connected[b].update(cbs)

    for cb in list(cbs):
        cx1, cx2 = cb[0][0], cb[1][0]
        cy1, cy2 = cb[0][1], cb[1][1]
        cz1, cz2 = cb[0][2], cb[1][2]

        supporting = set([])

        for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
            for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                if (x, y, cz1 - 1) in occupied:
                    supporting.add(occupied[(x, y, cz1 - 1)])
        if b not in supporting:
            print(b, supporting, cb)
            raise
        supported[cb].update(supporting)
        if len(supporting) == 1:
            can_hold = False
            only_connected[b].add(cb)

print(len([x for x in only_connected.values() if not x]))

def count_falling(b):
    removed = set([b])

    check = True
    while check:
        check = False
        for rb in list(removed):
            for cb in connected[rb]:
                if not cb in removed and len(supported[cb] - removed) == 0:
                    removed.add(cb)
                    check = True
    return len(removed) - 1

print(sum(count_falling(b) for b in fallen))
