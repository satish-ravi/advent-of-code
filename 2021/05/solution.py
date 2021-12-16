import sys
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, str_rep: str) -> "Point":
        xstr, ystr = str_rep.split(",")
        return cls(int(xstr), int(ystr))

    def __hash__(self) -> int:
        return hash(f"{self.x},{self.y}")


@dataclass
class Line:
    p1: Point
    p2: Point

    @classmethod
    def from_str(cls, str_rep: str) -> "Line":
        p1_str, p2_str = str_rep.split(" -> ")
        return cls(Point.from_str(p1_str), Point.from_str(p2_str))

    def is_horizontal_or_vertical(self) -> bool:
        return self.p1.x == self.p2.x or self.p1.y == self.p2.y

    def get_points(self) -> list[Point]:
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y

        assert dx == 0 or dy == 0 or abs(dx) == abs(dy)

        dir_x = dx // abs(dx) if dx else 0
        dir_y = dy // abs(dy) if dy else 0

        points = []
        for i in range(max(abs(dx), abs(dy)) + 1):
            points.append(Point(self.p1.x + dir_x * i, self.p1.y + dir_y * i))
        return points


def read_input() -> list[Line]:
    return list(Line.from_str(l.strip()) for l in sys.stdin.readlines())


def compute(lines: list[Line], filter_diagonals=False) -> int:
    points_count = defaultdict(int)

    for line in lines:
        if not filter_diagonals or line.is_horizontal_or_vertical():
            for point in line.get_points():
                points_count[point] += 1

    result = 0
    for point, count in points_count.items():
        if count >= 2:
            result += 1
    return result


inp = read_input()
print("part1:", compute(inp, True))
print("part2:", compute(inp, False))
