import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())


def get_next_sequence(seq):
    if all(x == 0 for x in seq):
        return 0
    diff_seq = []
    for i in range(len(seq) - 1):
        diff_seq.append(seq[i + 1] - seq[i])
    # res = seq[-1] + get_next_sequence(diff_seq)
    res = seq[0] - get_next_sequence(diff_seq)
    return res

ans = 0
for r, row in enumerate(inp):
    ans += get_next_sequence([int(n) for n in row.split(' ')])

print(ans)
