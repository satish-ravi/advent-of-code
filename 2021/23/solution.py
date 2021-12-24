import sys
from copy import deepcopy
from dataclasses import dataclass
from heapq import heappop, heappush

ROOM_POS = [3, 5, 7, 9]
HALLWAY_POS = [1, 2, 4, 6, 8, 10, 11]


COST_MAP = {"A": 1, "B": 10, "C": 100, "D": 1000}


def amphipod_to_room_pos(amphipod: str) -> int:
    return (ord(amphipod) - 64) * 2 + 1


def is_dest(amphipod: str, pos: int) -> bool:
    return amphipod_to_room_pos(amphipod) == pos


def replace_str(src: str, pos: int, val: str) -> str:
    as_list = list(src)
    as_list[pos] = val
    return "".join(as_list)


@dataclass
class State:
    rows: list[str]
    hallway: str

    def is_final_state(self) -> bool:
        for room_pos in ROOM_POS:
            for row in self.rows:
                if not is_dest(row[room_pos], room_pos):
                    return False
        return True

    def __str__(self) -> str:
        res = "#############\n"
        res += self.hallway + "\n"
        for row in self.rows:
            res += row + "\n"
        res += "  #########  "
        return res

    def __hash__(self) -> int:
        return hash("".join(self.rows) + self.hallway)

    def is_col_partially_complete(self, col: int) -> bool:
        return all(row[col] == "." or is_dest(row[col], col) for row in self.rows)

    def get_hallway_pos(self, empty: bool = False) -> list[int]:
        return [pos for pos in HALLWAY_POS if (self.hallway[pos] == ".") == empty]

    def has_hallway_path(self, start: int, end: int) -> bool:
        return all(self.hallway[pos] == "." for pos in range(start, end))

    def create_neighbor(self, hallway_pos: int, room_pos: int, row_index: int) -> tuple[int, "State"]:
        amphipod = self.hallway[hallway_pos] if self.hallway[hallway_pos] != "." else self.rows[row_index][room_pos]

        neighbor = State(deepcopy(self.rows), self.hallway)
        neighbor.hallway = replace_str(self.hallway, hallway_pos, self.rows[row_index][room_pos])
        neighbor.rows[row_index] = replace_str(self.rows[row_index], room_pos, self.hallway[hallway_pos])

        movement = abs(hallway_pos - room_pos) + row_index + 1

        return (movement * COST_MAP[amphipod], neighbor)

    def get_neighbors(self) -> list[tuple[int, "State"]]:
        neighbors = []
        for room_pos in ROOM_POS:
            if self.is_col_partially_complete(room_pos):
                continue

            cur_row_index = None
            for i, row in enumerate(self.rows):
                if row[room_pos] != ".":
                    cur_row_index = i
                    break
            if cur_row_index is None:
                continue
            amphipod = self.rows[cur_row_index][room_pos]
            dest_room_pos = amphipod_to_room_pos(amphipod)

            if self.is_col_partially_complete(dest_room_pos) and self.has_hallway_path(
                min(room_pos, dest_room_pos), max(room_pos, dest_room_pos + 1)
            ):
                dest_row = len(self.rows) - 1
                while dest_row >= 0 and self.rows[dest_row][dest_room_pos] != ".":
                    dest_row -= 1

                neighbor = State(deepcopy(self.rows), self.hallway)
                neighbor.rows[cur_row_index] = replace_str(self.rows[cur_row_index], room_pos, ".")
                neighbor.rows[dest_row] = replace_str(self.rows[dest_row], dest_room_pos, amphipod)
                movement = abs(dest_room_pos - room_pos) + cur_row_index + 1 + dest_row + 1
                neighbors.append((movement * COST_MAP[amphipod], neighbor))
            else:
                for hallway_pos in self.get_hallway_pos(True):
                    if self.has_hallway_path(min(hallway_pos, room_pos), max(hallway_pos, room_pos) + 1):
                        neighbors.append(self.create_neighbor(hallway_pos, room_pos, cur_row_index))

        for hallway_pos in self.get_hallway_pos(False):
            dest_room_pos = amphipod_to_room_pos(self.hallway[hallway_pos])

            if self.is_col_partially_complete(dest_room_pos) and self.has_hallway_path(
                min(hallway_pos, dest_room_pos) + 1, max(hallway_pos, dest_room_pos)
            ):
                dest_row = len(self.rows) - 1
                while dest_row >= 0 and self.rows[dest_row][dest_room_pos] != ".":
                    dest_row -= 1

                neighbors.append(self.create_neighbor(hallway_pos, dest_room_pos, dest_row))

        return neighbors


@dataclass
class Node:
    state: State
    cost: int
    path: list[tuple[int, State]]

    def __lt__(self, other: "Node"):
        return self.cost < other.cost


def read_input() -> list[str]:
    return [l.rstrip() for l in sys.stdin.readlines()]


def solve(state: State, print_path: bool = False) -> int:
    visited = set()
    queue = [Node(state, 0, [])]
    costs = {state: 0}

    while queue:
        cur = heappop(queue)
        if cur.state not in visited:
            visited.add(cur.state)
            if cur.state.is_final_state():
                if print_path:
                    for cost, state in cur.path:
                        print(state, cost)
                return cur.cost
            for ncost, neighbor in cur.state.get_neighbors():
                if neighbor in visited:
                    continue
                new_cost = cur.cost + ncost
                prev_cost = costs.get(neighbor, None)

                if prev_cost is None or new_cost < prev_cost:
                    costs[neighbor] = new_cost
                    heappush(queue, Node(neighbor, new_cost, [*cur.path, (cur.cost, cur.state)]))

    raise Exception("no path")


def part1(inp) -> int:
    state = State([inp[2], inp[3]], inp[1])
    return solve(state)


def part2(inp) -> int:
    state = State([inp[2], "  #D#C#B#A#", "  #D#B#A#C#", inp[3]], inp[1])
    return solve(state)


inp = read_input()
print("part1:", part1(inp))
print("part2:", part2(inp))
