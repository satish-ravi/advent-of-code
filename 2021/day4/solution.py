import sys
from dataclasses import dataclass

BOARD_SIZE = 5
BINGOS = []
for i in range(BOARD_SIZE):
    row = []
    column = []
    for j in range(BOARD_SIZE):
        row.append((i, j))
        column.append((j, i))
    BINGOS.append(row)
    BINGOS.append(column)

@dataclass
class Element:
    num: int
    marked: bool = False

class Board:
    board: list[list[Element]]

    def __init__(self, lines):
        self.board = []
        for line in lines:
            row = [Element(int(n)) for n in line.split()]
            assert len(row) == BOARD_SIZE
            self.board.append(row)
        assert len(self.board) == BOARD_SIZE

    def mark(self, num) -> bool:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c].num == num:
                    self.board[r][c].marked = True
                    return True
        return False

    def is_bingo(self) -> bool:
        for bingo in BINGOS:
            if all(self.board[r][c].marked for (r, c) in bingo):
                return True
        return False

    def score(self, last_num: int) -> int:
        unmarked_sum = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not self.board[i][j].marked:
                    unmarked_sum += self.board[i][j].num
        return unmarked_sum * last_num


def read_input() -> tuple[list[Board], list[int]]:
    inp = list(l.strip() for l in sys.stdin.readlines())

    draw = [int(n) for n in inp[0].split(",")]
    boards = []
    for i in range((len(inp) - 1) // (BOARD_SIZE + 1)):
        board_lines = [inp[(i * (BOARD_SIZE + 1)) + 2 + j] for j in range(BOARD_SIZE)]
        boards.append(Board(board_lines))
    return boards, draw

def compute(boards: list[Board], draw: list[int]) -> None:
    bingos_set = set()
    for num in draw:
        for i, board in enumerate(boards):
            if i in bingos_set:
                continue
            board.mark(num)
            if board.is_bingo():
                bingos_set.add(i)
                if len(bingos_set) == 1:
                    print('part1:', board.score(num))
                elif len(bingos_set) == len(boards):
                    print('part2:', board.score(num))
                    return

boards, draw = read_input()
compute(boards, draw)
