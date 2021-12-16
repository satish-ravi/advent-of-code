import sys


def read_input() -> list[str]:
    return [line.strip() for line in sys.stdin.readlines()]


PAIRS = {"]": "[", "}": "{", ")": "(", ">": "<"}


def part1(inp):
    points = {"]": 57, "}": 1197, ")": 3, ">": 25137}
    result = 0
    for line in inp:
        stack = []
        error = None
        for ch in line:
            if ch in PAIRS:
                if stack.pop() != PAIRS[ch]:
                    error = ch
                    break
            else:
                stack.append(ch)
        if error:
            result += points[error]
    return result


def part2(inp):
    points = {"(": 1, "[": 2, "{": 3, "<": 4}
    scores = []
    for line in inp:
        stack = []
        error = None
        for ch in line:
            if ch in PAIRS:
                if stack.pop() != PAIRS[ch]:
                    error = ch
                    break
            else:
                stack.append(ch)
        if not error and stack:
            score = 0
            while len(stack):
                score = score * 5 + points[stack.pop()]
            scores.append(score)
    return sorted(scores)[len(scores) // 2]


inp = read_input()
print("part1:", part1(inp))
print("part2:", part2(inp))
