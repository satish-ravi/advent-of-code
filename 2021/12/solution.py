from copy import deepcopy
import sys
from collections import defaultdict
from collections import deque, Counter
from typing import Callable


def read_input():
    connections = defaultdict(set)
    for line in sys.stdin.readlines():
        (a, b) = line.strip().split("-")
        connections[a].add(b)
        connections[b].add(a)
    return connections


def part1_original(connections: dict[str, set[str]]) -> int:
    all_paths = []
    queue = deque([("start", ["start"])])

    while len(queue):
        cur, cur_path = queue.popleft()
        if cur == "end":
            all_paths.append(",".join(cur_path))
            continue
        for next in connections[cur]:
            if next.isupper() or next not in cur_path:
                queue.append((next, cur_path + [next]))

    return len(all_paths)


def part2_original(connections: dict[str, set[str]]) -> int:
    all_paths = []
    queue = deque([("start", ["start"], False)])

    while len(queue):
        cur, cur_path, small_cave_twice = queue.popleft()
        if cur == "end":
            all_paths.append(",".join(cur_path))
            continue
        counter = Counter(cur_path)
        for next in connections[cur]:
            if (
                next.isupper()
                or next not in cur_path
                or (next != "start" and not small_cave_twice and counter[next] < 2)
            ):
                queue.append(
                    (
                        next,
                        cur_path + [next],
                        (small_cave_twice or (next.islower() and counter[next] == 1)),
                    )
                )

    return len(all_paths)


def count_all_paths(connections: dict[str, set[str]], should_skip: Callable):
    queue = deque([("start", {"start": 1})])
    n_paths = 0

    while queue:
        cur, visited_counts = queue.popleft()
        if cur == "end":
            n_paths += 1
            continue
        for next in connections[cur]:
            if next == "start" or should_skip(next, visited_counts):
                continue
            new_visited = deepcopy(visited_counts)
            new_visited[next] = new_visited.get(next, 0) + 1
            queue.append((next, new_visited))

    return n_paths


def part1_skip(cave: str, visited_counts: dict[str, int]) -> bool:
    return cave.islower() and cave in visited_counts


def part2_skip(cave: str, visited_counts: dict[str, int]) -> bool:
    return (
        cave.islower()
        and cave in visited_counts
        and any(cv.islower() and count == 2 for cv, count in visited_counts.items())
    )


inp = read_input()
print("part1:", part1_original(inp))
print("part2:", part2_original(inp))
print("part1:", count_all_paths(inp, part1_skip))
print("part2:", count_all_paths(inp, part2_skip))
