import sys
import math
from collections import defaultdict

inp = list(l for l in sys.stdin.readlines())

def parse_input(inp):
    return [tuple(map(int, line.split(','))) for line in inp]

def get_distance(box1, box2):
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.groups = n

    def find(self, x: int) -> int:
        # Path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # Union by rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        self.groups -= 1

    def get_groups(self):
        return self.groups

def part1(boxes):
    distances = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            distance = get_distance(boxes[i], boxes[j])
            distances.append((distance, i, j))
    distances.sort()

    uf = UnionFind(len(boxes))

    for i in range(1000):
        uf.union(distances[i][1], distances[i][2])
    groups = defaultdict(int)
    for i in range(len(boxes)):
        groups[uf.find(i)] += 1
    groups_sizes = list(groups.values())
    groups_sizes.sort()
    return groups_sizes[-1] * groups_sizes[-2] * groups_sizes[-3]

def part2(boxes):
    distances = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            distance = get_distance(boxes[i], boxes[j])
            distances.append((distance, i, j))
    distances.sort()

    uf = UnionFind(len(boxes))

    last_connected = None
    total_connected = 0
    while uf.get_groups() > 1:
        distance, i, j = distances.pop(0)
        uf.union(i, j)
        total_connected += 1
        last_connected = (boxes[i], boxes[j])
    return last_connected[0][0] * last_connected[1][0]

boxes = parse_input(inp)
print('part1:', part1(boxes))
print('part2:', part2(boxes))
