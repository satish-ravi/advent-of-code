import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())

ts = [int(n) for n in inp[0].split(': ')[1].strip().split(' ') if n]
ds = [int(n) for n in inp[1].split(': ')[1].strip().split(' ') if n]

ans = 1
for (t, d) in zip(ts, ds):
    w = 0
    for h in range(1, t):
        if h * (t-h) > d:
            w += 1
    if w:
        ans *= w
print(ans)

t = int(''.join(str(n) for n in ts))
d = int(''.join(str(n) for n in ds))
w = 0
for h in range(1, t):
    if h * (t-h) > d:
        w += 1
print(w)
