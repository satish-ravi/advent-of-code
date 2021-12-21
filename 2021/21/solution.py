import itertools
import sys
from collections import defaultdict
from functools import cache


def read_input() -> tuple[int, int]:
    lines = sys.stdin.readlines()

    p1 = int(lines[0].strip().split(": ")[-1])
    p2 = int(lines[1].strip().split(": ")[-1])

    return p1, p2


class DeterministicDie:
    rolls: int
    value: int

    def __init__(self):
        self.rolls = 0
        self.value = 0

    def roll(self) -> int:
        self.value = 1 if self.value == 100 else self.value + 1
        self.rolls += 1
        return self.value


def mod10(num: int) -> int:
    return (num - 1) % 10 + 1


def part1(p1: int, p2: int) -> int:
    die = DeterministicDie()

    positions = [p1, p2]
    scores = [0, 0]
    turn = 0

    while max(scores) < 1000:
        roll = 0
        for _ in range(3):
            roll += die.roll()
        positions[turn] = mod10(positions[turn] + roll)
        scores[turn] += positions[turn]
        turn = (turn + 1) % 2

    return scores[turn] * die.rolls


ROLLS_TO_UNIVS = defaultdict(int)

for rolls in itertools.product([1, 2, 3], repeat=3):
    ROLLS_TO_UNIVS[sum(rolls)] += 1


@cache
def get_wins_and_losses(
    current_pos: int, opponent_pos: int, current_score: int, opponent_score: int
) -> int:
    if opponent_score >= 21:
        return 0, 1
    wins, losses = 0, 0
    for rolls, univ in ROLLS_TO_UNIVS.items():
        new_pos = mod10(current_pos + rolls)
        new_losses, new_wins = get_wins_and_losses(
            opponent_pos, new_pos, opponent_score, current_score + new_pos
        )
        wins += new_wins * univ
        losses += new_losses * univ
    return wins, losses


def part2(p1: int, p2: int) -> int:
    return max(get_wins_and_losses(p1, p2, 0, 0))


p1, p2 = read_input()
print("part1:", part1(p1, p2))
print("part2:", part2(p1, p2))
