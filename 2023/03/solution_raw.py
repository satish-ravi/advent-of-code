import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())

ans = 0
part_num_pos = {}
for r, row in enumerate(inp):
    cur_num = ''
    is_part = False
    for c, ch in enumerate(row):
        if len(cur_num) and not ch.isdigit():
            if is_part:
                ans += int(cur_num)
                for col_num in range(c-len(cur_num), c):
                    part_num_pos[(r, col_num)] = int(cur_num)
            is_part = False
            cur_num = ''
        if ch.isdigit():
            cur_num += ch
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    ar = dr + r
                    ac = dc + c
                    if (ar < 0 or ac < 0 or ar >= len(inp) or ac >= len(row)):
                        continue
                    if (not inp[ar][ac].isdigit() and inp[ar][ac] != '.'):
                        is_part = True
    if len(cur_num) and is_part:
        ans += int(cur_num)
        for col_num in range(len(row)-len(cur_num), len(row)):
            part_num_pos[(r, col_num)] = int(cur_num)

print(ans)

ans = 0
for r, row in enumerate(inp):
    for c, ch in enumerate(row):
        if ch == '*':
            nums = set()
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    ar = dr + r
                    ac = dc + c
                    if (ar < 0 or ac < 0 or ar >= len(inp) or ac >= len(row)):
                        continue
                    if (ar, ac) in part_num_pos:
                        nums.add(part_num_pos[(ar, ac)])
            if (len(nums)) == 2:
                n = list(nums)
                ans += n[0] * n[1]
print(ans)