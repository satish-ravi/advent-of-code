import sys
from dataclasses import dataclass


@dataclass
class Sea:
    sea: dict[tuple[int, int], str]
    height: int
    width: int

    def get_next(self, r: int, c: int, ch: str) -> tuple[int, int]:
        if ch == ">":
            return (r, (c + 1) % (self.width))
        elif ch == "v":
            return ((r + 1) % (self.height), c)


def read_input() -> Sea:
    height = 0
    width = 0
    sea = {}
    for r, line in enumerate(sys.stdin.readlines()):
        for c, ch in enumerate(line.strip()):
            if ch != ".":
                sea[(r, c)] = ch
            width = c + 1
        height = r + 1
    return Sea(sea, height, width)


def do_step(sea: Sea, ch: str) -> tuple[Sea, bool]:
    next_sea = {}
    has_moved = False
    for (r, c), v in sea.sea.items():
        nr, nc = sea.get_next(r, c, v)
        if v == ch and (nr, nc) not in sea.sea:
            next_sea[(nr, nc)] = v
            has_moved = True
        else:
            next_sea[(r, c)] = v
    return Sea(next_sea, sea.height, sea.width), has_moved


def part1(sea: Sea) -> int:
    cnt = 0
    has_moved_right = True
    has_moved_down = True
    while has_moved_right or has_moved_down:
        sea, has_moved_right = do_step(sea, ">")
        sea, has_moved_down = do_step(sea, "v")
        cnt += 1
    return cnt


sea = read_input()
print("part1:", part1(sea))
