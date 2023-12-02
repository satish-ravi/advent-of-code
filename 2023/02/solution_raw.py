import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())

res = 0
max_cubs = {
    'red': 12,
    'green': 13,
    'blue': 14
}
print(len(inp))
for (i,l) in enumerate(inp):
    p = True
    rs = l.split(": ")[1].split("; ")
    for r in rs:
        cs = r.split(', ')
        for c in cs:
            [n, col] = c.split(' ')
            if int(n) > max_cubs[col]:
                p = False
                break
    if p:
        res += i + 1
print(res)

res = 0
for (i,l) in enumerate(inp):
    max_req = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    rs = l.split(": ")[1].split("; ")
    for r in rs:
        cs = r.split(', ')
        for c in cs:
            [n, col] = c.split(' ')
            max_req[col] = max(max_req[col], int(n))
    res += max_req['red'] * max_req['green'] * max_req['blue']
print(res)
