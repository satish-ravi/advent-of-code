import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0
part_num_pos = {}
for r, row in enumerate(inp):
    w, m = row.split(': ')[1].split(' | ')

    w = set([int(n.strip()) for n in w.split(' ') if n])
    m = set([int(n.strip()) for n in m.split(' ') if n])
    n = m.intersection(w)
    if (len(n) >= 1):
        ans += 2 ** (len(n)-1)

print(ans)

cards = {n: 1 for n in range(1, len(inp)+ 1)}

for r, row in enumerate(inp):
    w, m = row.split(': ')[1].split(' | ')

    w = set([int(n.strip()) for n in w.split(' ') if n])
    m = set([int(n.strip()) for n in m.split(' ') if n])
    n = m.intersection(w)

    for c in range(r+2, r+len(n)+2):
        if not c in cards:
            cards[c] = 0
        cards[c] += cards[r+1]

ans = 0
for n, v in cards.items():
    ans += v
print(ans)
