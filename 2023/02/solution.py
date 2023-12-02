import sys
import re
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    def is_greater(self, other):
        return self.red > other.red or self.green > other.green or self.blue > other.blue

    def power(self):
        return self.red * self.green * self.blue

@dataclass
class Game:
    id: int
    reveals: list[CubeSet]

    def get_min_set_power(self):
        min_set = CubeSet()
        for reveal in self.reveals:
            min_set.red = max(min_set.red, reveal.red)
            min_set.green = max(min_set.green, reveal.green)
            min_set.blue = max(min_set.blue, reveal.blue)
        return min_set.power()


def parse_input(raw_games):
    games = []
    for (index, game) in enumerate(raw_games):
        reveals = []
        raw_reveals = game.split(": ")[1].split("; ")
        for reveal in raw_reveals:
            cubes = reveal.split(', ')
            reveal_dict = {}
            for cube in cubes:
                [num, color] = cube.split(' ')
                reveal_dict[color] = int(num)
            reveals.append(CubeSet(**reveal_dict))
        games.append(Game(index + 1, reveals))
    return games

def part1(games):
    max_reveal = CubeSet(12, 13, 14)
    return sum(game.id for game in games if not any(reveal.is_greater(max_reveal) for reveal in game.reveals))

def part2(games):
    return sum(game.get_min_set_power() for game in games)

games = parse_input(inp)
print('part1:', part1(games))
print('part2:', part2(games))
