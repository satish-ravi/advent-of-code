import sys

inp = list(int(l.strip()) for l in sys.stdin.readlines())


def count_n_back_increasing(arr, n):
    return sum(arr[i] > arr[i - n] for i in range(n, len(arr)))


print("part1:", count_n_back_increasing(inp, 1))
print("part2:", count_n_back_increasing(inp, 3))
