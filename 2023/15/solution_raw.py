import sys

inp = list(l.strip() for l in sys.stdin.readlines())

ops = inp[0].split(',')

def get_hash(st):
    v = 0
    for c in st:
        v += ord(c)
        v *= 17
        v = v % 256
    return v

ans = 0
for r, row in enumerate(ops):
    ans+=get_hash(row)
print(ans)

boxes = [[] for i in range(256)]

for row in ops:
    if '-' in row:
        lb = row.split('-')[0]
        box = get_hash(lb)
        nb = []
        for x, f in boxes[box]:
            if x != lb:
                nb.append([x, f])
        boxes[box] = nb
    else:
        lb, fs = row.split("=")
        box = get_hash(lb)
        found = False
        for v in boxes[box]:
            if v[0] == lb:
                found = True
                v[1] = int(fs)
                break
        if not found:
            boxes[box].append([lb, int(fs)])
ans = 0
for b, box in enumerate(boxes):
    for c, v in enumerate(box):
        ans += (b+1) * (c+1) * v[1]
print(ans)

