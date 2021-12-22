import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class Cuboid:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def is_valid(self) -> bool:
        return self.x2 >= self.x1 and self.y2 >= self.y1 and self.z2 >= self.z1

    def overlaps(self, other: "Cuboid") -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
            and self.z1 <= other.z2
            and self.z2 >= other.z1
        )

    def volume(self) -> int:
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def _intersect(self, other: "Cuboid") -> "Cuboid":
        assert self.overlaps(other)

        return Cuboid(
            max(self.x1, other.x1),
            min(self.x2, other.x2),
            max(self.y1, other.y1),
            min(self.y2, other.y2),
            max(self.z1, other.z1),
            min(self.z2, other.z2),
        )

    def get_broken(self, other: "Cuboid") -> list["Cuboid"]:
        inter = self._intersect(other)

        broken: list["Cuboid"] = []
        # 6 centers:
        broken.append(Cuboid(other.x1, inter.x1 - 1, inter.y1, inter.y2, inter.z1, inter.z2))
        broken.append(Cuboid(inter.x2 + 1, other.x2, inter.y1, inter.y2, inter.z1, inter.z2))
        broken.append(Cuboid(inter.x1, inter.x2, other.y1, inter.y1 - 1, inter.z1, inter.z2))
        broken.append(Cuboid(inter.x1, inter.x2, inter.y2 + 1, other.y2, inter.z1, inter.z2))
        broken.append(Cuboid(inter.x1, inter.x2, inter.y1, inter.y2, other.z1, inter.z1 - 1))
        broken.append(Cuboid(inter.x1, inter.x2, inter.y1, inter.y2, inter.z2 + 1, other.z2))

        # 12 edges
        broken.append(Cuboid(inter.x1, inter.x2, other.y1, inter.y1 - 1, other.z1, inter.z1 - 1))
        broken.append(Cuboid(inter.x1, inter.x2, inter.y2 + 1, other.y2, inter.z2 + 1, other.z2))
        broken.append(Cuboid(inter.x1, inter.x2, inter.y2 + 1, other.y2, other.z1, inter.z1 - 1))
        broken.append(Cuboid(inter.x1, inter.x2, other.y1, inter.y1 - 1, inter.z2 + 1, other.z2))
        broken.append(Cuboid(other.x1, inter.x1 - 1, inter.y1, inter.y2, other.z1, inter.z1 - 1))
        broken.append(Cuboid(inter.x2 + 1, other.x2, inter.y1, inter.y2, inter.z2 + 1, other.z2))
        broken.append(Cuboid(inter.x2 + 1, other.x2, inter.y1, inter.y2, other.z1, inter.z1 - 1))
        broken.append(Cuboid(other.x1, inter.x1 - 1, inter.y1, inter.y2, inter.z2 + 1, other.z2))
        broken.append(Cuboid(other.x1, inter.x1 - 1, other.y1, inter.y1 - 1, inter.z1, inter.z2))
        broken.append(Cuboid(inter.x2 + 1, other.x2, inter.y2 + 1, other.y2, inter.z1, inter.z2))
        broken.append(Cuboid(inter.x2 + 1, other.x2, other.y1, inter.y1 - 1, inter.z1, inter.z2))
        broken.append(Cuboid(other.x1, inter.x1 - 1, inter.y2 + 1, other.y2, inter.z1, inter.z2))

        # 8 corners
        broken.append(Cuboid(other.x1, inter.x1 - 1, other.y1, inter.y1 - 1, other.z1, inter.z1 - 1))
        broken.append(Cuboid(inter.x2 + 1, other.x2, other.y1, inter.y1 - 1, other.z1, inter.z1 - 1))
        broken.append(Cuboid(other.x1, inter.x1 - 1, inter.y2 + 1, other.y2, other.z1, inter.z1 - 1))
        broken.append(Cuboid(inter.x2 + 1, other.x2, inter.y2 + 1, other.y2, other.z1, inter.z1 - 1))
        broken.append(Cuboid(other.x1, inter.x1 - 1, other.y1, inter.y1 - 1, inter.z2 + 1, other.z2))
        broken.append(Cuboid(inter.x2 + 1, other.x2, other.y1, inter.y1 - 1, inter.z2 + 1, other.z2))
        broken.append(Cuboid(other.x1, inter.x1 - 1, inter.y2 + 1, other.y2, inter.z2 + 1, other.z2))
        broken.append(Cuboid(inter.x2 + 1, other.x2, inter.y2 + 1, other.y2, inter.z2 + 1, other.z2))

        broken = [b for b in broken if b.is_valid()]

        assert other.volume() == inter.volume() + sum(b.volume() for b in broken)

        return broken


class Reactor:
    on_cuboids: list[Cuboid]

    def __init__(self) -> None:
        self.on_cuboids = []

    def on(self, cuboid: Cuboid) -> None:
        to_add = [cuboid]

        for on_cuboid in self.on_cuboids:
            new_to_add = []
            for cuboid in to_add:
                if on_cuboid.overlaps(cuboid):
                    new_to_add.extend(on_cuboid.get_broken(cuboid))
                else:
                    new_to_add.append(cuboid)
            to_add = new_to_add

        self.on_cuboids.extend(to_add)

    def off(self, cuboid: Cuboid) -> None:
        new_on = []

        for on_cuboid in self.on_cuboids:
            if on_cuboid.overlaps(cuboid):
                new_on.extend(cuboid.get_broken(on_cuboid))
            else:
                new_on.append(on_cuboid)

        self.on_cuboids = new_on

    def total_on(self) -> int:
        return sum(cuboid.volume() for cuboid in self.on_cuboids)


def read_input() -> list[tuple[str, Cuboid]]:
    inp = []
    for line in sys.stdin.readlines():
        ins, pos = line.strip().split(" ")
        x, y, z = pos.split(",")
        x1, x2 = [int(v) for v in x.split("=")[-1].split("..")]
        y1, y2 = [int(v) for v in y.split("=")[-1].split("..")]
        z1, z2 = [int(v) for v in z.split("=")[-1].split("..")]

        inp.append((ins, Cuboid(x1, x2, y1, y2, z1, z2)))

    return inp


def solve_bruteforce(inp: list[tuple[str, Cuboid]], bound: int = 50) -> int:
    states = {}

    get_range = lambda v1, v2: range(max(v1, -bound), min(v2, bound) + 1)

    for ins, cuboid in inp:
        for x in get_range(cuboid.x1, cuboid.x2):
            for y in get_range(cuboid.y1, cuboid.y2):
                for z in get_range(cuboid.z1, cuboid.z2):
                    states[(x, y, z)] = ins == "on"
    return len([item for item in states.values() if item])


def solve(inp: list[tuple[str, Cuboid]], bound: Optional[int] = None) -> int:
    reactor = Reactor()
    for ins, cuboid in inp:
        if bound:
            cuboid = Cuboid(
                max(cuboid.x1, -bound),
                min(cuboid.x2, bound),
                max(cuboid.y1, -bound),
                min(cuboid.y2, bound),
                max(cuboid.z1, -bound),
                min(cuboid.z2, bound),
            )
            if not cuboid.is_valid():
                continue
        if ins == "on":
            reactor.on(cuboid)
        else:
            reactor.off(cuboid)
    return reactor.total_on()


inp = read_input()
print("part1:", solve(inp, 50))
print("part2:", solve(inp))
