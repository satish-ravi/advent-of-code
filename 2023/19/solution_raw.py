import sys
from collections import deque
import functools
inp = list(l.strip() for l in sys.stdin.readlines())

wfs = {}
pts = []

end_wfs = False

for r, row in enumerate(inp):
    if row == '':
        end_wfs = True
        continue

    if end_wfs:
        pt = row[1:-1].split(',')
        pts.append({
            'x': int(pt[0].split('=')[-1]),
            'm': int(pt[1].split('=')[-1]),
            'a': int(pt[2].split('=')[-1]),
            's': int(pt[3].split('=')[-1])
        })
    else:
        wf, r = row[:-1].split('{')
        wfs[wf] = r

ans = 0

for pt in pts:
    wfn = 'in'
    while wfn not in ['A', 'R']:
        rs = wfs[wfn]
        rls = rs.split(',')
        fnd = False
        for rl in rls[:-1]:
            cnd,res = rl.split(':')
            s = cnd[0]
            op = cnd[1]
            v = int(cnd[2:])
            if op == '<' and pt[s] < v or op == '>' and pt[s] > v:
                wfn = res
                fnd = True
                break
        if not fnd:
            wfn = rls[-1]
    if wfn == 'A':
        ans += pt['x'] + pt['m'] + pt['a'] + pt['s']
print(ans)

# @functools.lru_cache(maxsize=None)
def solve(rng, wf):
    if any([r2 < r1 for r1, r2 in list(rng)]):
        return 0
    if wf == 'R':
        return 0
    if wf == 'A':
        ans = 1
        for r1, r2 in rng:
            ans *= r2-r1+1
        return ans
    ans = 0
    cr = rng
    rls = wfs[wf].split(',')
    for rl in rls[:-1]:
        cnd,res = rl.split(':')
        s = cnd[0]
        op = cnd[1]
        v = int(cnd[2:])
        nr1 = list(cr)
        nr2 = list(cr)
        md = 'xmas'.index(s)
        x1, x2 = cr[md]

        if op == '<':
            nr1[md] = (x1, v - 1)
            nr2[md] = (v, x2)
        else:
            nr1[md] = (v +1,x2)
            nr2[md] = (x1, v)
        ans += solve(tuple(nr1), res)
        cr = tuple(nr2)
    ans += solve(cr, rls[-1])
    return ans

print(solve(((1, 4000), (1, 4000), (1, 4000), (1, 4000)), 'in'))

ans = 0
q = deque([(((1, 4000), (1, 4000), (1, 4000), (1, 4000)), 'in')])

while q:
    rng, wf = q.popleft()

    if any([r2 < r1 for r1, r2 in rng]):
        continue
    if wf == 'R':
        continue
    if wf == 'A':
        cans = 1
        for r1, r2 in rng:
            cans *= r2-r1+1
        ans += cans
        continue

    cr = rng
    rls = wfs[wf].split(',')
    # print(rls)
    for rl in rls[:-1]:
        cnd,res = rl.split(':')
        s = cnd[0]
        op = cnd[1]
        v = int(cnd[2:])
        nr1 = list(cr)
        nr2 = list(cr)
        md = 'xmas'.index(s)
        x1, x2 = cr[md]

        if op == '<':
            nr1[md] = (x1, v - 1)
            nr2[md] = (v, x2)
        else:
            nr1[md] = (v +1,x2)
            nr2[md] = (x1, v)
        q.append((tuple(nr1), res))
        cr = tuple(nr2)
    q.append((cr, rls[-1]))
    # print(q)
    # break

print(ans)