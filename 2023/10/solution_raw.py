import sys
import re
from collections import deque

inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0
s = None
for r in range(len(inp)):
    for c in range(len(inp[r])):
        if inp[r][c] == 'S':
            s = (r, c)
            break
    if s:
        break

st = 'L' # for my input
# st = '7' # for p2 last test
# st = 'F' # for p2 last but one test
inp[r] = inp[r].replace('S', st)

q = deque()
q.append(s)

res = {s: 0}

while q:
    (cr, cc) = q.popleft()
    if cr != 0 and inp[cr][cc] in ['|', 'L', 'J']:
        nx = (cr - 1, cc)
        if nx not in res and inp[cr-1][cc] != '.':
            q.append(nx)
            res[nx] = res[(cr, cc)] + 1
    if cr != len(inp) - 1 and inp[cr][cc] in ['|', 'F', '7']:
        nx = (cr + 1, cc)
        if nx not in res and inp[cr+1][cc] != '.':
            q.append(nx)
            res[nx] = res[(cr, cc)] + 1
    if cc != 0 and inp[cr][cc] in ['-', 'J', '7']:
        nx = (cr, cc - 1)
        if nx not in res and inp[cr][cc-1] != '.':
            q.append(nx)
            res[nx] = res[(cr, cc)] + 1
    if cc != len(inp[0]) - 1 and inp[cr][cc] in ['-', 'F', 'L']:
        nx = (cr, cc + 1)
        if nx not in res and inp[cr][cc+1] != '.':
            q.append(nx)
            res[nx] = res[(cr, cc)] + 1

print(max(res.values()))

loop = [s]

cur = s
dir = 'R' if st in ['F', 'L'] else 'L'

while len(loop) == 1 or cur != s:
    (cr, cc) = cur
    if dir == 'R':
        nr, nc = cr, cc + 1
        nx_val = inp[nr][nc]
        if nx_val == '-':
            ndir = dir
        elif nx_val == 'J':
            ndir = 'U'
        elif nx_val == '7':
            ndir = 'D'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    elif dir == 'L':
        nr, nc = cr, cc - 1
        nx_val = inp[nr][nc]
        if nx_val == '-':
            ndir = dir
        elif nx_val == 'F':
            ndir = 'D'
        elif nx_val == 'L':
            ndir = 'U'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    elif dir == 'U':
        nr, nc = cr - 1, cc
        nx_val = inp[nr][nc]
        if nx_val == '|':
            ndir = dir
        elif nx_val == 'F':
            ndir = 'R'
        elif nx_val == '7':
            ndir = 'L'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    elif dir == 'D':
        nr, nc = cr + 1, cc
        nx_val = inp[nr][nc]
        if nx_val == '|':
            ndir = dir
        elif nx_val == 'J':
            ndir = 'L'
        elif nx_val == 'L':
            ndir = 'R'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    else:
        print('unknown dir', dir, cur)
        raise
    cur = (nr, nc)
    dir = ndir
    loop.append(cur)

temp = [['.' for _ in range(len(inp[0]) + 2)] for _ in range(len(inp) + 2)]

for (r, c) in loop:
    temp[r+1][c+1] = inp[r][c]

stack = [(0, 0)]

first_f = None
for r in range(len(temp)):
    for c in range(len(temp[0])):
        if temp[r][c] == 'F':
            first_f = (r,c)
            break
    if first_f:
        break

print(first_f)
loop2 = [first_f]

cur = first_f
dir = 'R'

while len(loop2) == 1 or cur != first_f:
    (cr, cc) = cur
    if dir == 'R':
        nr, nc = cr, cc + 1
        nx_val = temp[nr][nc]
        stack.append((cr - 1, cc))
        if nx_val == '-':
            ndir = dir
        elif nx_val == 'J':
            stack.append((cr - 1, cc + 1))
            ndir = 'U'
        elif nx_val == '7':
            stack.append((cr - 1, cc + 1))
            stack.append((cr - 1, cc + 2))
            ndir = 'D'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    elif dir == 'L':
        nr, nc = cr, cc - 1
        nx_val = temp[nr][nc]
        stack.append((cr + 1, cc))
        if nx_val == '-':
            ndir = dir
        elif nx_val == 'F':
            stack.append((cr + 1, cc - 1))
            ndir = 'D'
        elif nx_val == 'L':
            stack.append((cr + 1, cc - 1))
            stack.append((cr + 1, cc - 2))
            ndir = 'U'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    elif dir == 'U':
        nr, nc = cr - 1, cc
        nx_val = temp[nr][nc]
        stack.append((cr, cc - 1))
        if nx_val == '|':
            ndir = dir
        elif nx_val == 'F':
            stack.append((cr - 1, cc - 1))
            stack.append((cr - 2, cc - 1))
            ndir = 'R'
        elif nx_val == '7':
            stack.append((cr - 1, cc - 1))
            ndir = 'L'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    elif dir == 'D':
        nr, nc = cr + 1, cc
        nx_val = temp[nr][nc]
        stack.append((cr, cc + 1))
        if nx_val == '|':
            ndir = dir
        elif nx_val == 'J':
            stack.append((cr + 1, cc + 1))
            stack.append((cr + 2, cc + 1))
            ndir = 'L'
        elif nx_val == 'L':
            stack.append((cr + 1, cc + 1))
            ndir = 'R'
        else:
            print('impossible movement', cur, dir, nx_val)
            raise
    else:
        print('unknown dir', dir, cur)
        raise
    cur = (nr, nc)
    dir = ndir
    loop2.append(cur)

while stack:
    r, c = stack.pop()
    if not(0 <= r < len(temp) and 0 <= c < len(temp[0])) or temp[r][c] != '.':
        continue
    temp[r][c] = 'O'
    stack.append((r + 1, c))
    stack.append((r - 1, c))
    stack.append((r, c + 1))
    stack.append((r, c - 1))

for row in temp:
    print(''.join(row))

ans = 0
for row in temp:
    for val in row:
        if val == '.':
            ans += 1
print(ans)
