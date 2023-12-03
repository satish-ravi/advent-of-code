import sys
import abc
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass(frozen=True)
class Element(abc.ABC):
    row: int
    col: int

    @abc.abstractmethod
    def end_col(self):
        pass

    def col_range(self):
        return range(self.col, self.end_col() + 1)

    def get_adjacent_cells(self, nr, nc):
        adjacent = []
        col_ranges = list(self.col_range())
        if self.col != 0:
            col_ranges.append(self.col - 1)
            adjacent.append((self.row, self.col - 1))
        if self.end_col() != nc - 1:
            col_ranges.append(self.end_col() + 1)
            adjacent.append((self.row, self.end_col() + 1))
        if self.row != 0:
            for c in col_ranges:
                adjacent.append((self.row - 1, c))
        if self.row != nr - 1:
            for c in col_ranges:
                adjacent.append((self.row + 1, c))
        return set(adjacent)

@dataclass(frozen=True)
class Number(Element):
    number: int

    def end_col(self):
        return self.col + len(str(self.number)) - 1

@dataclass(frozen=True)
class Symbol(Element):
    symbol: str

    def end_col(self):
        return self.col


def parse_input(inp):
    symbols = []
    numbers = []
    for r, row in enumerate(inp):
        cur_num = ''
        for c, ch in enumerate(row):
            if ch.isdigit():
                cur_num += ch
            else:
                if ch != '.':
                    symbols.append(Symbol(symbol = ch, row = r, col = c))
                if cur_num:
                    numbers.append(Number(number = int(cur_num), row = r, col = c - len(cur_num)))
                    cur_num = ''
        if cur_num:
            numbers.append(Number(number = int(cur_num), row = r, col = len(row) - len(cur_num)))
    return numbers, symbols, len(inp), len(inp[0])

def part1(numbers, symbols, nr, nc):
    symbol_positions = set((symbol.row, symbol.col) for symbol in symbols)
    return sum(number.number for number in numbers if symbol_positions.intersection(number.get_adjacent_cells(nr, nc)))

def part2(numbers, symbols, nr, nc):
    numbers_by_positions = {}
    for number in numbers:
        for col in number.col_range():
            numbers_by_positions[(number.row, col)] = number

    result = 0
    for symbol in symbols:
        adjacent_numbers = set(numbers_by_positions[(r, c)] for r, c in symbol.get_adjacent_cells(nr, nc) if (r, c) in numbers_by_positions)
        if (len(adjacent_numbers) == 2):
            adjacent_list = list(adjacent_numbers)
            result += adjacent_list[0].number * adjacent_list[1].number
    return result


numbers, symbols, nr, nc = parse_input(inp)

print('part1:', part1(numbers, symbols, nr, nc))
print('part2:', part2(numbers, symbols, nr, nc))
